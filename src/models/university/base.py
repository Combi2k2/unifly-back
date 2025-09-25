from pydantic import BaseModel, Field, field_validator
from typing import Optional

# ========================
# Core University Entities
# ========================
#
# NOTE: ACCREDITATION POLICY
# --------------------------
# This application only works with accredited programs and institutions.
# Accreditation fields have been removed from all models as we assume
# all data in our system represents accredited educational programs.
# This simplifies the data model and ensures data quality.

class Location(BaseModel):
    """Location information for physical entities"""
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    coordinates: Optional[str] = Field(None, max_length=50)  # e.g., "40.7128,-74.0060"

class Contact(BaseModel):
    """Contact information for entities"""
    website: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    
    @field_validator('website')
    @classmethod
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Website must start with http:// or https://')
        return v

# University types as string constants
UNIVERSITY_TYPE_PUBLIC = "public"
UNIVERSITY_TYPE_PRIVATE = "private"
UNIVERSITY_TYPE_COMMUNITY = "community"
UNIVERSITY_TYPE_FOR_PROFIT = "for_profit"
UNIVERSITY_TYPE_NON_PROFIT = "non_profit"

# =====================
# University Metrics
# =====================

class EduStats(BaseModel):
    # Enrollment Statistics
    total_enrollment: Optional[int] = Field(None, ge=0)
    undergraduate_enrollment: Optional[int] = Field(None, ge=0)
    graduate_enrollment: Optional[int] = Field(None, ge=0)
    international_enrollment: Optional[int] = Field(None, ge=0)
    
    # Staff and Faculty Statistics
    student_per_staff_ratio: Optional[float] = Field(None, ge=0.0)
    total_staff: Optional[int] = Field(None, ge=0)
    faculty_count: Optional[int] = Field(None, ge=0)
    
    # Demographics
    international_ratio: Optional[float] = Field(None, ge=0.0, le=1.0)
    female_ratio: Optional[float] = Field(None, ge=0.0, le=1.0)
    male_ratio: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    # Additional Statistics
    acceptance_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    graduation_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    retention_rate: Optional[float] = Field(None, ge=0.0, le=1.0)

class EduScore(BaseModel):
    # Overall Scores
    overall_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    world_ranking: Optional[int] = Field(None, ge=1)
    national_ranking: Optional[int] = Field(None, ge=1)
    
    # Subject-Specific Scores
    teaching_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    research_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    citation_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    industry_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    international_outlook_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    
    # Additional Metrics
    reputation_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    employer_reputation_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    academic_reputation_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    
    # Ranking Year
    ranking_year: Optional[int] = Field(None, ge=2000, le=2030)

class University(BaseModel):
    university_id: int
    name: str = Field(..., min_length=1, max_length=255)
    type: str
    alias: str = Field(..., max_length=50)
    # NOTE: Accreditation field removed - we only use accredited programs in our application
    
    location: Location
    contact: Optional[Contact] = None
    
    # Additional university information (from UniInfo)
    overview: Optional[str] = Field(None, min_length=1, max_length=8000)
    history: Optional[str] = Field(None, min_length=1, max_length=8000)
    other: Optional[str] = Field(None, min_length=1, max_length=8000)
    
    # Metrics (from UniInfo)
    stats: Optional[EduStats] = None
    score: Optional[EduScore] = None

# =====================
# Academic Structure
# =====================

class Faculty(BaseModel):
    faculty_id: int
    university_id: int
    name: str = Field(..., min_length=1, max_length=255)
    desc: Optional[str] = Field(None, max_length=8000)
    alias: Optional[str] = Field(None, max_length=50)
    other: Optional[str] = Field(None, max_length=8000)
    contact: Optional[Contact] = None

class Department(BaseModel):
    department_id: int
    university_id: int
    faculty_id: int
    name: str = Field(..., min_length=1, max_length=255)
    desc: Optional[str] = Field(None, max_length=8000)
    alias: Optional[str] = Field(None, max_length=50)
    other: Optional[str] = Field(None, max_length=8000)
    contact: Optional[Contact] = None

# =====================
# Core University Models
# =====================
# Note: Other models have been moved to separate files:
# - uniAcademic.py: Course
# - uniProgram.py: Program
# - uniPeople.py: Person, Staff
# - uniResearch.py: ResearchLab, ResearchProject, ResearchProjectMember
