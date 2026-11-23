from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class Frequency(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

class ResolutionStatus(Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"

############################################
# Classes are defined here
############################################
class UserCreate(BaseModel):
    email: str
    fullName: str
    lastLoginAt: Optional[datetime] = None
    progressEntries: Optional[List[int]] = None  # 1:N Relationship
    habits: Optional[List[int]] = None  # 1:N Relationship
    resolutions: Optional[List[int]] = None  # 1:N Relationship


class SubGoalCreate(BaseModel):
    completed: bool
    description: Optional[str] = None
    targetDate: Optional[date] = None
    title: str
    parentResolution: int  # N:1 Relationship (mandatory)


class ResolutionCreate(BaseModel):
    description: Optional[str] = None
    status: ResolutionStatus
    targetDate: Optional[date] = None
    title: str
    category: Optional[int] = None  # N:1 Relationship (optional)
    owner: int  # N:1 Relationship (mandatory)
    subGoals: Optional[List[int]] = None  # 1:N Relationship
    progressEntries: Optional[List[int]] = None  # 1:N Relationship


class ProgressEntryCreate(BaseModel):
    amount: Optional[float] = None
    date: datetime
    notes: Optional[str] = None
    author: int  # N:1 Relationship (mandatory)
    habit: Optional[int] = None  # N:1 Relationship (optional)
    resolution: Optional[int] = None  # N:1 Relationship (optional)


class HabitCreate(BaseModel):
    active: bool
    currentStreak: int
    description: Optional[str] = None
    frequency: Frequency
    lastDoneAt: Optional[datetime] = None
    name: str
    progressEntries: Optional[List[int]] = None  # 1:N Relationship
    habitUser: int  # N:1 Relationship (mandatory)


class CategoryCreate(BaseModel):
    colorHex: Optional[str] = None
    name: str
    resolutions: Optional[List[int]] = None  # 1:N Relationship


