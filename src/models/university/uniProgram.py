from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .base import Contact, EduStats, EduScore

# =====================
# Program Models
# =====================

# Program levels as string constants
PROGRAM_LEVEL_BACHELOR = "bachelor"
PROGRAM_LEVEL_MASTER = "master"
PROGRAM_LEVEL_PHD = "phd"
PROGRAM_LEVEL_ASSOCIATE = "associate"
PROGRAM_LEVEL_CERTIFICATE = "certificate"
PROGRAM_LEVEL_DIPLOMA = "diploma"

class Program(BaseModel):
    program_id: int
    department_id: int
    name: str = Field(..., min_length=1, max_length=255)
    desc: str = Field(..., min_length=1, max_length=8000)
    level: str
    years: Optional[int] = Field(None, ge=1, le=10)
    contact: Optional[Contact] = None
    # NOTE: Accreditation field removed - we only use accredited programs in our application
    
    # Program metrics
    stats: Optional[EduStats] = None
    score: Optional[EduScore] = None
    
    # Reference links
    ref_tuition:   Optional[str] = Field(None, max_length=500)  # Link to tuition information
    ref_syllabus:  Optional[str] = Field(None, max_length=500)  # Link to syllabus/curriculum
    ref_admission: Optional[str] = Field(None, max_length=500)  # Link to admission requirements
    ref_outcome:   Optional[str] = Field(None, max_length=500)  # Link to learning outcomes/career prospects
    
    @field_validator('ref_tuition', 'ref_syllabus', 'ref_admission', 'ref_outcome')
    @classmethod
    def validate_urls(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Reference URLs must start with http:// or https://')
        return v