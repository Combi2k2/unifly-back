"""
SQL Repository for User Data
Handles interactions with SQL database for user data using SQLAlchemy
"""

import logging
from typing import Optional, List
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from contextlib import contextmanager

from models.user import UserBase, UserRole, UserStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserRepository:
    """Repository class to handle interactions with the SQL database for user data"""
    
    def __init__(self, connection_string: str, database_name: str = "unifly"):
        """
        Initialize the repository with SQL database connection parameters
        
        Args:
            connection_string: SQL database connection string (e.g., "postgresql://user:pass@localhost:5432")
            database_name: Name of the database to use (default: "unifly")
        """
        try:
            self.database_name = database_name
            
            # Create full URI for engine
            full_uri = f"{connection_string.rstrip('/')}/{database_name}"
            
            # Create engine
            self.engine = create_engine(
                full_uri,
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info(f"Successfully connected to SQL database: {self.database_name}")
            
            self._initialize_tables()
            
        except Exception as e:
            logger.error(f"Failed to connect to SQL database: {e}")
            raise
    
    def _initialize_tables(self):
        """Initialize tables and create indexes if they don't exist"""
        try:
            # Check if users table already exists
            with self.get_session() as session:
                result = session.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' 
                            AND table_name = 'users'
                        );
                    """)
                ).fetchone()
                
                table_exists = result[0] if result else False
                
                if table_exists:
                    logger.info("Users table already exists, skipping creation")
                    return
                
                logger.info("Users table does not exist, creating...")
            
            # Create metadata
            metadata = MetaData()
            
            # Define users table
            self.users_table = Table(
                'users',
                metadata,
                Column('userid', Integer, primary_key=True, index=True),
                Column('first_name', String(100), nullable=False),
                Column('last_name', String(100), nullable=False),
                Column('email', String(255), nullable=False, unique=True, index=True),
                Column('phone', String(20), nullable=True),
                Column('date_of_birth', DateTime, nullable=True),
                Column('nationality', String(100), nullable=True),
                Column('hashed_password', String(255), nullable=False),
                Column('role', SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT),
                Column('status', SQLEnum(UserStatus), nullable=False, default=UserStatus.PENDING_VERIFICATION),
                Column('profile_picture_url', String(500), nullable=True),
                Column('timezone', String(50), nullable=True),
                Column('language_preference', String(10), nullable=True, default='en'),
                Column('created_at', DateTime, nullable=False),
                Column('updated_at', DateTime, nullable=False)
            )
            
            # Create all tables
            metadata.create_all(self.engine)
            
            logger.info("Tables and indexes created successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize tables: {e}")
            raise
    
    @contextmanager
    def get_session(self):
        """Get database session with automatic cleanup"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def _convert_db_to_user(self, db_dict: dict) -> UserBase:
        """Convert database row to UserBase object, handling enum conversions"""
        # Convert uppercase database enum values back to lowercase for Pydantic
        user_dict = db_dict.copy()
        if 'role' in user_dict and isinstance(user_dict['role'], str):
            user_dict['role'] = user_dict['role'].lower()
        if 'status' in user_dict and isinstance(user_dict['status'], str):
            user_dict['status'] = user_dict['status'].lower()
        
        return UserBase(**user_dict)
    
    def close(self):
        """Close the database connection"""
        try:
            if self.engine:
                self.engine.dispose()
                logger.info("SQL database connection closed")
        except Exception as e:
            logger.error(f"Error closing SQL database connection: {e}")
    
    # ==================== User CRUD Methods ====================
    
    def upsert(self, user: UserBase) -> int:
        """
        Insert or update a user (upsert operation)
        
        Args:
            user: UserBase object to insert or update
            
        Returns:
            userid of the upserted user
            
        Raises:
            Exception: If upsert fails
        """
        try:
            with self.get_session() as session:
                # Prepare user data
                user_data = user.model_dump()
                
                # Convert enum values to strings (uppercase for database)
                if 'role' in user_data and hasattr(user_data['role'], 'value'):
                    user_data['role'] = user_data['role'].value.upper()
                if 'status' in user_data and hasattr(user_data['status'], 'value'):
                    user_data['status'] = user_data['status'].value.upper()
                
                # Use PostgreSQL UPSERT (ON CONFLICT DO UPDATE)
                result = session.execute(
                    text("""
                        INSERT INTO users (
                            userid, first_name, last_name, email, phone, date_of_birth, 
                            nationality, hashed_password, role, status, profile_picture_url, 
                            timezone, language_preference, created_at, updated_at
                        ) VALUES (
                            :userid, :first_name, :last_name, :email, :phone, :date_of_birth,
                            :nationality, :hashed_password, :role, :status, :profile_picture_url,
                            :timezone, :language_preference, NOW(), NOW()
                        )
                        ON CONFLICT (userid) DO UPDATE SET
                            first_name = EXCLUDED.first_name,
                            last_name = EXCLUDED.last_name,
                            email = EXCLUDED.email,
                            phone = EXCLUDED.phone,
                            date_of_birth = EXCLUDED.date_of_birth,
                            nationality = EXCLUDED.nationality,
                            hashed_password = EXCLUDED.hashed_password,
                            role = EXCLUDED.role,
                            status = EXCLUDED.status,
                            profile_picture_url = EXCLUDED.profile_picture_url,
                            timezone = EXCLUDED.timezone,
                            language_preference = EXCLUDED.language_preference,
                            updated_at = NOW()
                    """),
                    user_data
                )
                
                logger.info(f"Successfully upserted user with userid: {user.userid}")
                return user.userid
                
        except Exception as e:
            logger.error(f"Failed to upsert user {user.userid}: {e}")
            raise
    
    def remove(self, userid: int) -> bool:
        """
        Delete a user
        
        Args:
            userid: User ID to delete
            
        Returns:
            True if user was deleted, False otherwise
        """
        try:
            with self.get_session() as session:
                result = session.execute(
                    text("DELETE FROM users WHERE userid = :userid"),
                    {"userid": userid}
                )
                
                if result.rowcount > 0:
                    logger.info(f"Successfully deleted user {userid}")
                    return True
                else:
                    logger.warning(f"No user found to delete for userid: {userid}")
                    return False
                
        except Exception as e:
            logger.error(f"Failed to delete user {userid}: {e}")
            return False
    
    def exists(self, userid: int) -> bool:
        """
        Check if a user exists
        
        Args:
            userid: User ID to check
            
        Returns:
            True if user exists, False otherwise
        """
        try:
            with self.get_session() as session:
                result = session.execute(
                    text("SELECT 1 FROM users WHERE userid = :userid LIMIT 1"),
                    {"userid": userid}
                ).fetchone()
                
                return result is not None
                
        except Exception as e:
            logger.error(f"Failed to check if user {userid} exists: {e}")
            return False
    
    def get_by_id(self, userid: int) -> Optional[UserBase]:
        """
        Get a user by userid
        
        Args:
            userid: User ID to search for
            
        Returns:
            UserBase object if found, None otherwise
        """
        try:
            with self.get_session() as session:
                result = session.execute(
                    text("SELECT * FROM users WHERE userid = :userid"),
                    {"userid": userid}
                ).fetchone()
                
                if result:
                    # Convert result to dict
                    user_dict = dict(result._mapping)
                    return self._convert_db_to_user(user_dict)
                
                logger.info(f"No user found for userid: {userid}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user {userid}: {e}")
            return None

    def get_count(self) -> int:
        """
        Get total number of users
        
        Returns:
            Total count of users
        """
        try:
            with self.get_session() as session:
                result = session.execute(
                    text("SELECT COUNT(*) as count FROM users")
                ).fetchone()
                
                count = result.count if result else 0
                logger.info(f"Total user count: {count}")
                return count
                
        except Exception as e:
            logger.error(f"Failed to get user count: {e}")
            return 0
    
    def get_all(self) -> List[UserBase]:
        """
        Get all users
        
        Returns:
            List of UserBase objects
        """
        try:
            with self.get_session() as session:
                results = session.execute(
                    text("SELECT * FROM users ORDER BY userid")
                ).fetchall()
                
                users = []
                for result in results:
                    user_dict = dict(result._mapping)
                    users.append(self._convert_db_to_user(user_dict))
                
                logger.info(f"Retrieved {len(users)} users")
                return users
                
        except Exception as e:
            logger.error(f"Failed to get all users: {e}")
            return []
    
    def get_by_email(self, email: str) -> Optional[UserBase]:
        """
        Get a user by email
        
        Args:
            email: Email to search for
            
        Returns:
            UserBase object if found, None otherwise
        """
        try:
            with self.get_session() as session:
                result = session.execute(
                    text("SELECT * FROM users WHERE email = :email"),
                    {"email": email}
                ).fetchone()
                
                if result:
                    # Convert result to dict
                    user_dict = dict(result._mapping)
                    return self._convert_db_to_user(user_dict)
                
                logger.info(f"No user found for email: {email}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user by email {email}: {e}")
            return None
    
    def get_by_role(self, role: UserRole) -> List[UserBase]:
        """
        Get users by role
        
        Args:
            role: UserRole to filter by
            
        Returns:
            List of UserBase objects with the specified role
        """
        try:
            with self.get_session() as session:
                results = session.execute(
                    text("SELECT * FROM users WHERE role = :role ORDER BY userid"),
                    {"role": role.value.upper()}
                ).fetchall()
                
                users = []
                for result in results:
                    user_dict = dict(result._mapping)
                    users.append(self._convert_db_to_user(user_dict))
                
                logger.info(f"Retrieved {len(users)} users with role: {role.value}")
                return users
                
        except Exception as e:
            logger.error(f"Failed to get users by role {role.value}: {e}")
            return []
    
    def get_by_status(self, status: UserStatus) -> List[UserBase]:
        """
        Get users by status
        
        Args:
            status: UserStatus to filter by
            
        Returns:
            List of UserBase objects with the specified status
        """
        try:
            with self.get_session() as session:
                results = session.execute(
                    text("SELECT * FROM users WHERE status = :status ORDER BY userid"),
                    {"status": status.value.upper()}
                ).fetchall()
                
                users = []
                for result in results:
                    user_dict = dict(result._mapping)
                    users.append(self._convert_db_to_user(user_dict))
                
                logger.info(f"Retrieved {len(users)} users with status: {status.value}")
                return users
                
        except Exception as e:
            logger.error(f"Failed to get users by status {status.value}: {e}")
            return []
    
    def update_status(self, userid: int, status: UserStatus) -> bool:
        """
        Update user status
        
        Args:
            userid: User ID to update
            status: New status
            
        Returns:
            True if status was updated, False otherwise
        """
        try:
            with self.get_session() as session:
                result = session.execute(
                    text("UPDATE users SET status = :status, updated_at = NOW() WHERE userid = :userid"),
                    {"userid": userid, "status": status.value.upper()}
                )
                
                if result.rowcount > 0:
                    logger.info(f"Successfully updated user {userid} status to {status.value}")
                    return True
                else:
                    logger.warning(f"No user found to update status for userid: {userid}")
                    return False
                
        except Exception as e:
            logger.error(f"Failed to update user {userid} status: {e}")
            return False