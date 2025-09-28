from pydantic import BaseModel, Field
from typing import Optional
from .base import Contact

# =====================
# Research
# =====================

class ResearchLab(BaseModel):
    """Core Research Lab entity with comprehensive information"""
    lab_id: int
    department_id: int
    university_id: int
    name: str = Field(..., min_length=1, max_length=255)
    desc: str = Field(..., min_length=1, max_length=8000)
    contact: Optional[Contact] = None