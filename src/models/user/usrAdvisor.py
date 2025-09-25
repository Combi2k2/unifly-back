from pydantic import BaseModel, Field
from typing import Optional, List

# TODO: Implement advisor-specific models
# This file will contain advisor-specific data models when needed

class AdvisorProfile(BaseModel):
    """Placeholder for advisor profile model"""
    userid: int = Field(description="Unique identifier for the user")
    # Add advisor-specific fields here
    pass

class AdvisorPreference(BaseModel):
    """Placeholder for advisor preference model"""
    userid: int = Field(description="Unique identifier for the user")
    # Add advisor-specific preference fields here
    pass
