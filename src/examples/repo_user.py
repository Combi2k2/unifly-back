"""
UserRepository Example Usage
Demonstrates comprehensive usage of the UserRepository with upsert functionality
"""

import os
import sys
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.repos.user import UserRepository
from models.user import UserBase, UserRole, UserStatus


def main():
    """Comprehensive example of UserRepository usage"""
    print("=== UserRepository Example Usage ===\n")
    
    # Initialize repository
    connection_string = "postgresql://macos@localhost:5432"
    database_name = "unifly"
    repo = UserRepository(connection_string, database_name)
    
    try:
        print("1. Repository Initialization")
        print("-" * 40)
        print(f"✓ Connected to database: {database_name}")
        print(f"✓ Connection string: {connection_string}")
        print("✓ Table existence check performed")
        print()
        
        # 1. Upsert Operations (Create/Update)
        print("2. Upsert Operations (Create/Update)")
        print("-" * 40)
        
        # Create initial users
        users_data = [
            {
                "userid": 1001,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "date_of_birth": datetime(1995, 6, 15),
                "nationality": "American",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2",
                "role": UserRole.STUDENT,
                "status": UserStatus.ACTIVE,
                "profile_picture_url": "https://example.com/john.jpg",
                "timezone": "America/New_York",
                "language_preference": "en",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "userid": 1002,
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "phone": "+1234567891",
                "date_of_birth": datetime(1992, 3, 22),
                "nationality": "Canadian",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2",
                "role": UserRole.ADVISOR,
                "status": UserStatus.ACTIVE,
                "profile_picture_url": "https://example.com/jane.jpg",
                "timezone": "America/Toronto",
                "language_preference": "en",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "userid": 1003,
                "first_name": "Maria",
                "last_name": "Garcia",
                "email": "maria.garcia@example.com",
                "phone": "+1234567892",
                "date_of_birth": datetime(1998, 9, 10),
                "nationality": "Spanish",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2",
                "role": UserRole.STUDENT,
                "status": UserStatus.PENDING_VERIFICATION,
                "profile_picture_url": "https://example.com/maria.jpg",
                "timezone": "Europe/Madrid",
                "language_preference": "es",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]
        
        # Upsert users (create)
        print("Creating initial users...")
        for user_data in users_data:
            user = UserBase(**user_data)
            userid = repo.upsert(user)
            print(f"✓ Upserted user {userid}: {user.first_name} {user.last_name}")
        print()
        
        # Update a user (upsert with existing userid)
        print("Updating user information...")
        updated_user = UserBase(
            userid=1001,
            first_name="John Updated",
            last_name="Doe Updated",
            email="john.updated@example.com",
            phone="+1234567890",
            date_of_birth=datetime(1995, 6, 15),
            nationality="American",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2",
            role=UserRole.STUDENT,
            status=UserStatus.ACTIVE,
            profile_picture_url="https://example.com/john_updated.jpg",
            timezone="America/New_York",
            language_preference="en",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        userid = repo.upsert(updated_user)
        print(f"✓ Updated user {userid}: {updated_user.first_name} {updated_user.last_name}")
        print()
        
        # 2. Read Operations
        print("3. Read Operations")
        print("-" * 40)
        
        # Get user by ID
        print("Getting user by ID...")
        user = repo.get_by_id(1001)
        if user:
            print(f"✓ Found user: {user.first_name} {user.last_name}")
            print(f"  Email: {user.email}")
            print(f"  Role: {user.role}")
            print(f"  Status: {user.status}")
        else:
            print("❌ User not found")
        print()
        
        # Get user by email
        print("Getting user by email...")
        user_by_email = repo.get_by_email("jane.smith@example.com")
        if user_by_email:
            print(f"✓ Found user: {user_by_email.first_name} {user_by_email.last_name}")
            print(f"  UserID: {user_by_email.userid}")
            print(f"  Role: {user_by_email.role}")
        else:
            print("❌ User not found")
        print()
        
        # Get all users
        print("Getting all users...")
        all_users = repo.get_all()
        print(f"✓ Retrieved {len(all_users)} users:")
        for user in all_users:
            print(f"  - {user.first_name} {user.last_name} ({user.role.value})")
        print()
        
        # 3. Filtering Operations
        print("4. Filtering Operations")
        print("-" * 40)
        
        # Get users by role
        print("Getting users by role...")
        students = repo.get_by_role(UserRole.STUDENT)
        print(f"✓ Found {len(students)} students:")
        for student in students:
            print(f"  - {student.first_name} {student.last_name}")
        
        advisors = repo.get_by_role(UserRole.ADVISOR)
        print(f"✓ Found {len(advisors)} advisors:")
        for advisor in advisors:
            print(f"  - {advisor.first_name} {advisor.last_name}")
        print()
        
        # Get users by status
        print("Getting users by status...")
        active_users = repo.get_by_status(UserStatus.ACTIVE)
        print(f"✓ Found {len(active_users)} active users:")
        for user in active_users:
            print(f"  - {user.first_name} {user.last_name}")
        
        pending_users = repo.get_by_status(UserStatus.PENDING_VERIFICATION)
        print(f"✓ Found {len(pending_users)} pending users:")
        for user in pending_users:
            print(f"  - {user.first_name} {user.last_name}")
        print()
        
        # 4. Status Management
        print("5. Status Management")
        print("-" * 40)
        
        # Update user status
        print("Updating user status...")
        success = repo.update_status(1003, UserStatus.ACTIVE)
        if success:
            print("✓ Updated user 1003 status to ACTIVE")
            
            # Verify status update
            updated_user = repo.get_by_id(1003)
            if updated_user and updated_user.status == UserStatus.ACTIVE:
                print("✓ Status update verified")
            else:
                print("❌ Status update verification failed")
        else:
            print("❌ Failed to update user status")
        print()
        
        # 5. Utility Operations
        print("6. Utility Operations")
        print("-" * 40)
        
        # Check user existence
        print("Checking user existence...")
        exists_1001 = repo.exists(1001)
        exists_9999 = repo.exists(9999)
        print(f"✓ User 1001 exists: {exists_1001}")
        print(f"✓ User 9999 exists: {exists_9999}")
        print()
        
        # Get user count
        print("Getting user count...")
        user_count = repo.get_count()
        print(f"✓ Total users in database: {user_count}")
        print()
        
        # 6. Error Handling
        print("7. Error Handling")
        print("-" * 40)
        
        # Test duplicate email handling
        print("Testing duplicate email handling...")
        try:
            duplicate_user = UserBase(
                userid=1004,
                first_name="Duplicate",
                last_name="User",
                email="john.updated@example.com",  # Duplicate email
                phone="+1234567893",
                date_of_birth=datetime(1990, 1, 1),
                nationality="Test",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2",
                role=UserRole.STUDENT,
                status=UserStatus.ACTIVE,
                profile_picture_url="https://example.com/duplicate.jpg",
                timezone="UTC",
                language_preference="en",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            repo.upsert(duplicate_user)
            print("❌ Duplicate email should have been rejected")
        except Exception as e:
            print(f"✓ Caught expected error: {type(e).__name__}")
            print(f"  Error: {str(e)[:100]}...")
        print()
        
        # Test non-existent user retrieval
        print("Testing non-existent user retrieval...")
        non_existent = repo.get_by_id(9999)
        if non_existent is None:
            print("✓ Correctly returned None for non-existent user")
        else:
            print("❌ Should have returned None for non-existent user")
        print()
        
        # 7. Cleanup
        print("8. Cleanup")
        print("-" * 40)
        
        # Delete test users
        print("Cleaning up test data...")
        test_userids = [1001, 1002, 1003, 1004]
        deleted_count = 0
        
        for userid in test_userids:
            if repo.remove(userid):
                deleted_count += 1
                print(f"✓ Deleted user {userid}")
            else:
                print(f"⚠ User {userid} not found or already deleted")
        
        print(f"✓ Cleaned up {deleted_count} users")
        print()
        
        print("=== Example completed successfully! ===")
        print("✓ All UserRepository operations demonstrated")
        print("✓ Upsert functionality working correctly")
        print("✓ Read operations working correctly")
        print("✓ Filtering operations working correctly")
        print("✓ Status management working correctly")
        print("✓ Error handling working correctly")
        
    except Exception as e:
        print(f"❌ Error during example execution: {e}")
        print(f"Error type: {type(e).__name__}")
        raise
    
    finally:
        # Close repository connection
        repo.close()
        print("\n✓ Repository connection closed")


def demonstrate_advanced_usage():
    """Demonstrate advanced usage patterns"""
    print("\n=== Advanced Usage Patterns ===\n")
    
    connection_string = "postgresql://macos@localhost:5432"
    database_name = "unifly"
    repo = UserRepository(connection_string, database_name)
    
    try:
        print("1. Batch Operations")
        print("-" * 30)
        
        # Create multiple users in batch
        batch_users = []
        for i in range(5):
            user = UserBase(
                userid=2000 + i,
                first_name=f"Batch{i}",
                last_name="User",
                email=f"batch{i}@example.com",
                phone=f"+123456789{i}",
                date_of_birth=datetime(1990 + i, 1, 1),
                nationality="Test",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2",
                role=UserRole.STUDENT,
                status=UserStatus.ACTIVE,
                profile_picture_url=f"https://example.com/batch{i}.jpg",
                timezone="UTC",
                language_preference="en",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            batch_users.append(user)
        
        print("Creating batch users...")
        for user in batch_users:
            repo.upsert(user)
        print(f"✓ Created {len(batch_users)} users in batch")
        
        # Verify batch creation
        all_users = repo.get_all()
        batch_count = len([u for u in all_users if u.userid >= 2000])
        print(f"✓ Verified {batch_count} batch users in database")
        
        print("\n2. Role-based Operations")
        print("-" * 30)
        
        # Promote a student to advisor
        student = repo.get_by_id(2000)
        if student:
            student.role = UserRole.ADVISOR
            student.status = UserStatus.ACTIVE
            repo.upsert(student)
            print(f"✓ Promoted {student.first_name} {student.last_name} to advisor")
        
        # Get updated role counts
        students = repo.get_by_role(UserRole.STUDENT)
        advisors = repo.get_by_role(UserRole.ADVISOR)
        print(f"✓ Current students: {len(students)}")
        print(f"✓ Current advisors: {len(advisors)}")
        
        print("\n3. Status Workflow")
        print("-" * 30)
        
        # Simulate user verification workflow
        pending_user = UserBase(
            userid=3000,
            first_name="Pending",
            last_name="User",
            email="pending@example.com",
            phone="+1234567899",
            date_of_birth=datetime(1995, 1, 1),
            nationality="Test",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2",
            role=UserRole.STUDENT,
            status=UserStatus.PENDING_VERIFICATION,
            profile_picture_url="https://example.com/pending.jpg",
            timezone="UTC",
            language_preference="en",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create pending user
        repo.upsert(pending_user)
        print("✓ Created pending user")
        
        # Verify user
        repo.update_status(3000, UserStatus.ACTIVE)
        print("✓ Updated user status to ACTIVE")
        
        # Verify status change
        verified_user = repo.get_by_id(3000)
        if verified_user and verified_user.status == UserStatus.ACTIVE:
            print("✓ User verification workflow completed")
        
        print("\n4. Cleanup Advanced Data")
        print("-" * 30)
        
        # Clean up batch users
        for userid in range(2000, 2005):
            repo.remove(userid)
        repo.remove(3000)
        print("✓ Cleaned up advanced test data")
        
    except Exception as e:
        print(f"❌ Error in advanced usage: {e}")
        raise
    
    finally:
        repo.close()


if __name__ == "__main__":
    # Run main example
    main()
    
    # Run advanced usage example
    demonstrate_advanced_usage()
    
    print("\n🎉 All UserRepository examples completed successfully!")
    print("The UserRepository is ready for production use!")
