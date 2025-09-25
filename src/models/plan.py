from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal

# =====================
# Plan System - String Constants
# =====================

# Plan phases as string constants
PLAN_PHASE_PLANNING = "planning"
PLAN_PHASE_EXECUTION = "execution"
PLAN_PHASE_MONITORING = "monitoring"
PLAN_PHASE_EVALUATION = "evaluation"
PLAN_PHASE_CLOSURE = "closure"

# Task priorities as string constants
TASK_PRIORITY_LOW = "low"
TASK_PRIORITY_MEDIUM = "medium"
TASK_PRIORITY_HIGH = "high"
TASK_PRIORITY_URGENT = "urgent"

# Task status as string constants
TASK_STATUS_PENDING = "pending"
TASK_STATUS_IN_PROGRESS = "in_progress"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_OVERDUE = "overdue"
TASK_STATUS_CANCELLED = "cancelled"

# =====================
# Supporting Models for Comprehensive Plan System
# =====================

class Evaluation(BaseModel):
    """How success/failure is judged - defines criteria and records actual assessment results"""
    eval_criteria: str = Field(..., min_length=1, max_length=8000)
    eval_metrics: Dict[str, Any] = {}
    evaluator: Optional[str] = None
    score: Optional[float] = Field(None, ge=0.0, le=100.0)
    feedback: Optional[str] = None

class Goal(BaseModel):
    """Goals that can represent any level of objectives (high-level goals or specific objectives)"""
    goal_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    desc: str = Field(..., min_length=1, max_length=8000)
    priority: str = TASK_PRIORITY_MEDIUM
    end_date: Optional[date] = None
    evaluation: Optional[Evaluation] = None

    tags: List[str] = []  # For categorization and filtering
    
class Task(BaseModel):
    """Generic task that can represent any level of work breakdown"""
    task_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    desc: str = Field(..., min_length=1, max_length=8000)
    priority: str = TASK_PRIORITY_MEDIUM
    status:   str = TASK_STATUS_PENDING

    deliverables: str = Field(..., min_length=1, max_length=8000)
    
    # Timing
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    estimated_hours: Optional[int] = Field(None, ge=0)
    
    # Dependencies
    dependencies: List[int] = []  # Tasks this depends on
    
    # Notes
    notes: str = Field(..., min_length=1, max_length=1023)
    notes_progress: str = Field(..., min_length=1, max_length=1023)
    notes_complete: str = Field(..., min_length=1, max_length=1023)

    # Additional metadata
    tags: List[str] = []  # For categorization and filtering

# =====================
# Main Comprehensive Plan Model
# =====================

class Plan(BaseModel):
    """Comprehensive plan model covering all 8 structured sections"""
    
    # 1. Identity & Scope
    plan_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=255)
    scope: str = Field(..., min_length=0, max_length=8000)
    context: str = Field(..., min_length=0, max_length=8000)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    tags: List[str] = []  # For categorization and filtering
    
    # 2. Strategy
    notes_strategy: str = Field(..., min_length=1, max_length=1023)
    # Comprehensive strategy documentation including:
    # - Approach: General way to achieve objectives
    # - Key Principles: Rules that guide execution
    # - Assumptions: Things believed true but not certain
    # - Dependencies: External/internal factors the plan relies on
    
    # 3. Goals & Work Breakdown Structure
    vision_statement: Optional[str] = None  # The ultimate "why"
    goals: List[Goal] = []
    tasks: List[Task] = []
    # All work breakdown items (milestones, phases, tasks, deliverables, subtasks)
    
    # 4. Execution & Monitoring
    progress_phase: str = PLAN_PHASE_PLANNING
    progress_notes: str = Field(..., min_length=1, max_length=1023)
    progress_pct: int = Field(0, ge=0, le=100)
    
    # 5. Evaluation & Closure
    closure_date: Optional[date] = None
    closure_notes: str = Field(..., min_length=1, max_length=1023)
    # Comprehensive closure documentation including:
    # - Lessons Learned: What was learned from the plan
    # - Next Steps: What to do next