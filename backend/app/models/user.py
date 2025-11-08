"""
User and Preferences Data Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, time
from enum import Enum


class CalendarProvider(str, Enum):
    GOOGLE = "google"
    OUTLOOK = "outlook"


class NotificationSettings(BaseModel):
    email: bool = True
    push: bool = True
    in_app: bool = True
    reminder_minutes_before: List[int] = [15, 60]


class AIPreferences(BaseModel):
    auto_schedule: bool = True
    priority_weights: Dict[str, float] = {
        "deadline": 0.4,
        "importance": 0.4,
        "duration": 0.2,
    }


class UserPreferencesBase(BaseModel):
    work_hours_start: Optional[time] = time(9, 0)
    work_hours_end: Optional[time] = time(17, 0)
    work_days: Optional[List[int]] = [1, 2, 3, 4, 5]  # Monday to Friday
    preferred_break_duration: Optional[int] = 15  # minutes
    notification_settings: Optional[NotificationSettings] = NotificationSettings()
    calendar_sync_enabled: bool = False
    calendar_providers: Optional[List[CalendarProvider]] = []
    ai_preferences: Optional[AIPreferences] = AIPreferences()


class UserPreferencesUpdate(BaseModel):
    work_hours_start: Optional[time] = None
    work_hours_end: Optional[time] = None
    work_days: Optional[List[int]] = None
    preferred_break_duration: Optional[int] = None
    notification_settings: Optional[NotificationSettings] = None
    calendar_sync_enabled: Optional[bool] = None
    calendar_providers: Optional[List[CalendarProvider]] = None
    ai_preferences: Optional[AIPreferences] = None


class UserPreferences(UserPreferencesBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
