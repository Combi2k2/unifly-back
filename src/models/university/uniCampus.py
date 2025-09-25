from pydantic import BaseModel, Field
from typing import Optional, List
from .base import Contact, Location

# =====================
# Facilities & Resources
# =====================

# Facility types as string constants
FACILITY_TYPE_LIBRARY = "library"
FACILITY_TYPE_LABORATORY = "laboratory"
FACILITY_TYPE_DORMITORY = "dormitory"
FACILITY_TYPE_SPORTS_COMPLEX = "sports_complex"
FACILITY_TYPE_AUDITORIUM = "auditorium"
FACILITY_TYPE_CLASSROOM = "classroom"
FACILITY_TYPE_CAFETERIA = "cafeteria"
FACILITY_TYPE_ADMINISTRATIVE = "administrative"

class Facility(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    desc: str = Field(..., min_length=1, max_length=8000)
    type: str
    capacity: Optional[int] = Field(None, ge=0)
    contact: Optional[Contact] = None

# =====================
# Campus & Facilities
# =====================

class Campus(BaseModel):
    campus_id: int
    university_id: int
    name: str = Field(..., min_length=1, max_length=255)
    desc: str = Field(..., min_length=1, max_length=8000)
    facilities: List[Facility] = []
    location: Location
    contact: Optional[Contact] = None