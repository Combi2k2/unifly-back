# from __future__ import annotations

# from pydantic import BaseModel, Field
# from typing import Optional
# from decimal import Decimal
# from .base import Contact

# class Course(BaseModel):
#     course_id: int
#     code: str = Field(..., min_length=1, max_length=20)
#     name: str = Field(..., min_length=1, max_length=255)
#     desc: Optional[str] = None
#     credits: Optional[Decimal] = Field(None, ge=0.0, le=10.0)
#     semester: Optional[str] = Field(None, max_length=50)
#     contact: Optional[Contact] = None
