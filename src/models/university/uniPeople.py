from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from .base import Contact

# =====================
# People
# =====================

# Gender options as string constants
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_OTHER = "other"
GENDER_PREFER_NOT_TO_SAY = "prefer_not_to_say"

class Person(BaseModel):
    person_id: Optional[int] = None
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    contact: Optional[Contact] = None
    about: Optional[str] = Field(None, max_length=8000)
    other: Optional[str] = Field(None, max_length=8000)