"""
Note Data Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SourceType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"


class NoteBase(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: str
    source_type: SourceType = SourceType.TEXT
    media_url: Optional[str] = None
    transcription: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    transcription: Optional[str] = None
    extracted_tasks: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class Note(NoteBase):
    id: str
    user_id: str
    extracted_tasks: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
