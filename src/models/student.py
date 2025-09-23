from pydantic import BaseModel, Field
from typing import Optional, List

class Education(BaseModel):
    name:   str = Field(description = "Name of the school where the student attended")
    period: str = Field(description = "Period when student attend this school, in format mm/yy-mm/yy")
    gpa:    float = Field(description = "GPA that the student obtained during this period, normalized to 4.0 scale. If not available, return -1")
    degree: str = Field(description = "Degree that the student obtained during this period. If not available, return None")
    major:  Optional[str]= Field(description = "Major that the student obtained during this period. If not available, return None")

class Experience(BaseModel):
    name:   str = Field(description = "Job title and name of the company/institution")
    period: str = Field(description = "Period of this experience, in format mm/yy-mm/yy. The ending date can be 'present'.")
    desc:   str = Field(description = "Description of the achievement during this period")

class Award(BaseModel):
    name: str = Field(description = "Name of the competition")
    desc: str = Field(description = "Brief description and earned title in the competition")
    date: str = Field(description = "The time of the competition, in format mm/yy")

class ExtraCurricular(BaseModel):
    name:   str = Field(description = "Title and name of the project/organization")
    period: str = Field(description = "Period of this experience, in format mm/yy-mm/yy. The ending date can be 'present'.")
    desc:   str = Field(description = "Description of the achievement during this period")

class StandardizedTest(BaseModel):
    name:  str   = Field(description = "Name of the standardized test")
    score: float = Field(description = "Student's score in the test")
    date:  str   = Field(description = "The time of the test, in format mm/yy")

# Student Profile Schemas
class StudentProfile(BaseModel):
    userid: int = Field(description="Unique identifier for the user")
    gender: str = Field(description = "Gender of the student")
    overview: str = Field(description = "Short biography or description of the student")
    educations: List[Education] = []
    experience: List[Experience] = []
    activities: List[ExtraCurricular] = []
    standardized_tests: List[StandardizedTest] = []
    awards: List[Award] = []
    others: Optional[str] = Field(description = "Information shared by user that does not fall under other categories")

class StudentPreference(BaseModel):
    userid: int = Field(description="Unique identifier for the user")
    # Academic Interests
    intended_major:  List[str] = Field(description="Student's favorite majors in higer education")
    intended_degree: List[str] = Field(description="Student's intended degrees in higer education")
    
    # Location Preferences
    preferred_countries: List[str] = []
    preferred_cities: List[str] = []
    
    # Financial Information
    budget_min: Optional[int] = Field(None, ge=0, description="Minimum annual budget in USD for university expenses")
    budget_max: Optional[int] = Field(None, ge=0, description="Maximum annual budget in USD for university expenses")
    others: Optional[str] = Field(description="Information shared by user that does not fall under other categories")