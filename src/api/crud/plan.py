"""
Plan CRUD API Router

This module handles all CRUD operations for plan-related entities.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Import actual plan models
from src.models.plan import (
    Plan,
    Task,
    Goal,
    Evaluation
)

# Import CRUD operations
# from src.interface.crud.plan import PlanCRUD, TaskCRUD, etc.

plan_router = APIRouter()