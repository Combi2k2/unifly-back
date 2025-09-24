from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ApplicationPhase(str, Enum):
    RESEARCH = "research"
    PREPARATION = "preparation"
    APPLICATION = "application"
    SUBMISSION = "submission"
    REVIEW = "review"
    DECISION = "decision"
    ACCEPTANCE = "acceptance"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


# Application Task Schemas
class ApplicationTaskBase(BaseModel):
    # Task Information
    task_name: str = Field(..., min_length=1, max_length=300)
    task_description: Optional[str] = None
    task_phase: ApplicationPhase
    
    # Task Details
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    
    # Timing
    due_date: Optional[datetime] = None
    estimated_duration_hours: Optional[int] = Field(None, ge=0)
    actual_time_spent_hours: Optional[int] = Field(None, ge=0)
    
    # Task Dependencies
    depends_on_tasks: Optional[List[int]] = None
    prerequisite_tasks: Optional[List[int]] = None
    
    # Task Details
    task_type: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    
    # Resources and Links
    resources: Optional[List[str]] = None
    instructions: Optional[str] = None
    tips: Optional[str] = None
    
    # Progress Tracking
    progress_notes: Optional[str] = None
    completion_notes: Optional[str] = None




# Application Plan Schemas
class ApplicationPlanBase(BaseModel):
    # Plan Information
    plan_name: str = Field(..., min_length=1, max_length=200)
    target_degree_level: str = Field(..., pattern="^(undergraduate|graduate|phd)$")
    target_start_year: int = Field(..., ge=2020, le=2030)
    target_start_season: str = Field(..., pattern="^(fall|spring|summer)$")
    
    # Timeline Information
    plan_start_date: Optional[datetime] = None
    plan_end_date: Optional[datetime] = None
    application_deadline: Optional[datetime] = None
    
    # Plan Status
    current_phase: ApplicationPhase = ApplicationPhase.RESEARCH
    completion_percentage: int = Field(0, ge=0, le=100)
    is_active: bool = True
    
    # Target Universities and Programs
    target_universities: Optional[List[str]] = None
    target_programs: Optional[List[str]] = None
    
    # Notes and Comments
    notes: Optional[str] = None
    special_requirements: Optional[str] = None


