"""
Configuration for Unifly Backend
Configuration variables loaded from YAML files (dev/prod)
"""

import yaml
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

def _load_config() -> Dict[str, Any]:
    """Load configuration from YAML file based on environment variable"""
    # Get environment from .env file, default to 'dev'
    env = os.getenv('environment', 'dev')
    config_file = f"config.{env}.yaml"
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', config_file)
    
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML configuration: {e}")

# Load configuration
_config = _load_config()

# =====================
# Database Configuration (MongoDB)
# =====================

# MongoDB Connection String
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/")
MONGODB_DATABASE_NAME = _config['databases']['mongodb']['database_name']

# MongoDB Collection Names
MONGODB_USER_BASE = _config['databases']['mongodb']['user_base']
MONGODB_STUDENT_PROFILES    = _config['databases']['mongodb']['student_profiles']
MONGODB_STUDENT_PREFERENCES = _config['databases']['mongodb']['student_preferences']
MONGODB_ADVISOR_PROFILES    = _config['databases']['mongodb']['advisor_profiles']
MONGODB_PARENT_PROFILES     = _config['databases']['mongodb']['parent_profiles']
MONGODB_ADMIN_PROFILES      = _config['databases']['mongodb']['admin_profiles']

MONGODB_UNIVERSITIES = _config['databases']['mongodb']['universities']
MONGODB_UNIVERSITY_FACULTIES    = _config['databases']['mongodb']['university_faculties']
MONGODB_UNIVERSITY_DEPARTMENTS  = _config['databases']['mongodb']['university_departments']
MONGODB_UNIVERSITY_CAMPUSES     = _config['databases']['mongodb']['university_campuses']
MONGODB_UNIVERSITY_PROGRAMS     = _config['databases']['mongodb']['university_programs']
MONGODB_UNIVERSITY_PEOPLE       = _config['databases']['mongodb']['university_people']
MONGODB_UNIVERSITY_RESEARCH     = _config['databases']['mongodb']['university_research']
MONGODB_UNIVERSITY_SCHOLARSHIPS = _config['databases']['mongodb']['university_scholarships']

MONGODB_PLANS = _config['databases']['mongodb']['plans']

# =====================
# Database Configuration (Qdrant)
# =====================

# Qdrant Connection Settings
QDRANT_URL = os.getenv("QDRANT_URL", None)  # Optional URL for cloud Qdrant
QDRANT_KEY = os.getenv("QDRANT_KEY", None)  # Optional key for cloud Qdrant

# Qdrant Collection Names
QDRANT_UNIVERSITIES = _config['databases']['qdrant']['universities']
QDRANT_UNIVERSITY_FACULTIES    = _config['databases']['qdrant']['university_faculties']
QDRANT_UNIVERSITY_DEPARTMENTS  = _config['databases']['qdrant']['university_departments']
QDRANT_UNIVERSITY_CAMPUSES     = _config['databases']['qdrant']['university_campuses']
QDRANT_UNIVERSITY_PROGRAMS     = _config['databases']['qdrant']['university_programs']
QDRANT_UNIVERSITY_PEOPLE       = _config['databases']['qdrant']['university_people']
QDRANT_UNIVERSITY_RESEARCH     = _config['databases']['qdrant']['university_research']
QDRANT_UNIVERSITY_SCHOLARSHIPS = _config['databases']['qdrant']['university_scholarships']

# =====================
# Application Configuration
# =====================

APP_NAME        = _config['app']['name']
APP_VERSION     = _config['app']['version']
APP_ENVIRONMENT = _config['app']['environment']
DEBUG = _config['app']['debug']
LOG_LEVEL = _config['app']['log_level']

# =====================
# API Configuration
# =====================

API_HOST = _config['api']['host']
API_PORT = _config['api']['port']
CORS_ORIGINS    = _config['api']['cors_origins']
RATE_LIMIT      = _config['api']['rate_limit']

# =====================
# Example Usage
# =====================

if __name__ == "__main__":
    print("Unifly Backend Configuration")
    print("=" * 40)
    
    print(f"\nEnvironment: {APP_ENVIRONMENT}")
    print(f"App: {APP_NAME} v{APP_VERSION}")
    print(f"Debug: {DEBUG}")
    print(f"Log Level: {LOG_LEVEL}")
    
    print("\nAPI Configuration:")
    print(f"  Host: {API_HOST}")
    print(f"  Port: {API_PORT}")
    print(f"  CORS Origins: {CORS_ORIGINS}")
    
    print("\nMongoDB Database Names:")
    print(f"  user_base: {MONGODB_USER_BASE}")
    print(f"  student_profiles: {MONGODB_STUDENT_PROFILES}")
    print(f"  student_preferences: {MONGODB_STUDENT_PREFERENCES}")
    print(f"  advisor_profiles: {MONGODB_ADVISOR_PROFILES}")
    print(f"  parent_profiles: {MONGODB_PARENT_PROFILES}")
    print(f"  admin_profiles: {MONGODB_ADMIN_PROFILES}")
    print(f"  universities: {MONGODB_UNIVERSITIES}")
    print(f"  university_campuses: {MONGODB_UNIVERSITY_CAMPUSES}")
    print(f"  university_programs: {MONGODB_UNIVERSITY_PROGRAMS}")
    print(f"  university_people: {MONGODB_UNIVERSITY_PEOPLE}")
    print(f"  university_research: {MONGODB_UNIVERSITY_RESEARCH}")
    print(f"  university_scholarships: {MONGODB_UNIVERSITY_SCHOLARSHIPS}")
    print(f"  university_faculties: {MONGODB_UNIVERSITY_FACULTIES}")
    print(f"  university_departments: {MONGODB_UNIVERSITY_DEPARTMENTS}")
    print(f"  plans: {MONGODB_PLANS}")
    
    print("\nQdrant Configuration:")
    print(f"  URL: {'Set' if QDRANT_URL else 'Not set'}")
    print(f"  Key: {'Set' if QDRANT_KEY else 'Not set'}")
    
    print("\nQdrant Collection Names:")
    print(f"  universities: {QDRANT_UNIVERSITIES}")
    print(f"  university_campuses: {QDRANT_UNIVERSITY_CAMPUSES}")
    print(f"  university_programs: {QDRANT_UNIVERSITY_PROGRAMS}")
    print(f"  university_people: {QDRANT_UNIVERSITY_PEOPLE}")
    print(f"  university_research: {QDRANT_UNIVERSITY_RESEARCH}")
    print(f"  university_scholarships: {QDRANT_UNIVERSITY_SCHOLARSHIPS}")
    print(f"  university_faculties: {QDRANT_UNIVERSITY_FACULTIES}")
    print(f"  university_departments: {QDRANT_UNIVERSITY_DEPARTMENTS}")