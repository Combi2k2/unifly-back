from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

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

class UniLocation(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=200)
    state: Optional[str] = Field(None, max_length=200)
    country: str = Field(..., min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)

class UniContact(BaseModel):
    website: str = Field(..., min_length=1, max_length=500)
    phone: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=255)
    
    @field_validator('website')
    @classmethod
    def validate_website(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Website must start with http:// or https://')
        return v

class UniInfo(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=500)
    overview: str = Field(..., min_length=1, max_length=10000)
    history:  str = Field(..., min_length=1, max_length=10000)
    
    location: UniLocation
    contact: UniContact

    stats: EduStats
    score: EduScore

    other_info: Optional[str] = Field(None, min_length=1, max_length=10000)
    
    # # Academic Information
    # total_programs: Optional[int] = Field(None, ge=0)
    # undergraduate_programs: Optional[int] = Field(None, ge=0)
    # graduate_programs: Optional[int] = Field(None, ge=0)
    # doctoral_programs: Optional[int] = Field(None, ge=0)
    
    # # Financial Information
    # tuition_in_state: Optional[float] = Field(None, ge=0.0)
    # tuition_out_state: Optional[float] = Field(None, ge=0.0)
    # tuition_international: Optional[float] = Field(None, ge=0.0)
    # room_board_cost: Optional[float] = Field(None, ge=0.0)
    # total_cost_estimate: Optional[float] = Field(None, ge=0.0)
    
    # # Application Information
    # application_deadline_fall: Optional[datetime] = None
    # application_deadline_spring: Optional[datetime] = None
    # application_deadline_summer: Optional[datetime] = None
    # early_decision_deadline: Optional[datetime] = None
    # early_action_deadline: Optional[datetime] = None
    
    # # Additional Information
    # campus_size: Optional[float] = Field(None, ge=0.0)
    # campus_setting: Optional[str] = Field(None, regex="^(urban|suburban|rural)$")
    # housing_available: Optional[str] = Field(None, regex="^(yes|no|limited)$")