from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date
from decimal import Decimal
from .base import Contact

# =====================
# Scholarship System Models
# =====================

# Provider types as string constants
PROVIDER_TYPE_GOVERNMENT = "government"
PROVIDER_TYPE_UNIVERSITY = "university"
PROVIDER_TYPE_NGO = "ngo"
PROVIDER_TYPE_PRIVATE_COMPANY = "private_company"
PROVIDER_TYPE_FOUNDATION = "foundation"
PROVIDER_TYPE_INTERNATIONAL_ORGANIZATION = "international_organization"
PROVIDER_TYPE_INDIVIDUAL_DONOR = "individual_donor"

class ScholarshipProvider(BaseModel):
    provider_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    type: str
    country: Optional[str] = Field(None, max_length=100)
    contact: Optional[Contact] = None

# Criteria types as string constants
CRITERIA_TYPE_GPA = "gpa"
CRITERIA_TYPE_NATIONALITY = "nationality"
CRITERIA_TYPE_INCOME_LEVEL = "income_level"
CRITERIA_TYPE_PROGRAM = "program"
CRITERIA_TYPE_DEGREE_LEVEL = "degree_level"
CRITERIA_TYPE_AGE = "age"
CRITERIA_TYPE_GENDER = "gender"
CRITERIA_TYPE_FIELD_OF_STUDY = "field_of_study"
CRITERIA_TYPE_ACADEMIC_ACHIEVEMENT = "academic_achievement"
CRITERIA_TYPE_FINANCIAL_NEED = "financial_need"
CRITERIA_TYPE_COMMUNITY_SERVICE = "community_service"
CRITERIA_TYPE_LEADERSHIP = "leadership"
CRITERIA_TYPE_SPORTS = "sports"
CRITERIA_TYPE_ARTS = "arts"
CRITERIA_TYPE_RESEARCH_INTEREST = "research_interest"

class ScholarshipEligibility(BaseModel):
    criteria_type: str
    criteria_value: str = Field(..., max_length=255)
    description: Optional[str] = None

# Scholarship categories as string constants
SCHOLARSHIP_TYPE_MERIT_BASED = "merit_based"
SCHOLARSHIP_TYPE_NEED_BASED = "need_based"
SCHOLARSHIP_TYPE_ATHLETIC = "athletic"
SCHOLARSHIP_TYPE_ACADEMIC = "academic"
SCHOLARSHIP_TYPE_RESEARCH = "research"
SCHOLARSHIP_TYPE_DIVERSITY = "diversity"
SCHOLARSHIP_TYPE_INTERNATIONAL = "international"
SCHOLARSHIP_TYPE_MINORITY = "minority"
SCHOLARSHIP_TYPE_FIRST_GENERATION = "first_generation"
SCHOLARSHIP_TYPE_FIELD_SPECIFIC = "field_specific"

class Scholarship(BaseModel):
    """Comprehensive scholarship model with flexible amount ranges"""
    scholarship_id: Optional[int] = None
    provider_id: int
    name: str = Field(..., min_length=1, max_length=255)
    desc: str = Field(..., min_length=1, max_length=8000)
    type: str

    amount_min: Optional[Decimal] = Field(None, ge=0.0)
    amount_max: Optional[Decimal] = Field(None, ge=0.0)
    currency: str = Field(default="USD", min_length=3, max_length=10)

    eligibility: List[ScholarshipEligibility] = []

    application_deadline: Optional[date] = None
    application_start_date: Optional[date] = None
    notification_date: Optional[date] = None
    contact: Contact = None

# =====================
# Scholarship Analytics and Reporting
# =====================

class ScholarshipMetrics(BaseModel):
    """Metrics and statistics for scholarship tracking"""
    scholarship_id: int
    total_applications: int = Field(0, ge=0)
    approved_applications: int = Field(0, ge=0)
    rejected_applications: int = Field(0, ge=0)
    pending_applications: int = Field(0, ge=0)
    total_amount_awarded: Decimal = Field(0.0, ge=0.0)
    average_award_amount: Optional[Decimal] = None
    application_success_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    last_updated: Optional[date] = None