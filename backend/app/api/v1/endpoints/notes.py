"""
Note Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.models.note import Note, NoteCreate, NoteUpdate
from app.api.dependencies import get_current_user
from app.core.supabase import supabase_client
import structlog
from datetime import datetime

router = APIRouter()
logger = structlog.get_logger()


@router.post("", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, current_user: dict = Depends(get_current_user)):
    """Create a new note"""
    try:
        note_data = note.model_dump()
        note_data["user_id"] = current_user["id"]
        note_data["created_at"] = datetime.utcnow().isoformat()
        note_data["updated_at"] = datetime.utcnow().isoformat()

        response = supabase_client.table("notes").insert(note_data).execute()

        logger.info("Note created", note_id=response.data[0]["id"], user_id=current_user["id"])
        return Note(**response.data[0])
    except Exception as e:
        logger.error("Failed to create note", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[Note])
async def list_notes(
    current_user: dict = Depends(get_current_user),
    source_type: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
):
    """List user's notes with optional filters"""
    try:
        query = supabase_client.table("notes").select("*").eq("user_id", current_user["id"])

        if source_type:
            query = query.eq("source_type", source_type)

        response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()

        return [Note(**note) for note in response.data]
    except Exception as e:
        logger.error("Failed to list notes", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific note"""
    try:
        response = (
            supabase_client.table("notes")
            .select("*")
            .eq("id", note_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        return Note(**response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get note", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{note_id}", response_model=Note)
async def update_note(
    note_id: str, note_update: NoteUpdate, current_user: dict = Depends(get_current_user)
):
    """Update a note"""
    try:
        update_data = note_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()

        response = (
            supabase_client.table("notes")
            .update(update_data)
            .eq("id", note_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        logger.info("Note updated", note_id=note_id, user_id=current_user["id"])
        return Note(**response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update note", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a note"""
    try:
        response = (
            supabase_client.table("notes")
            .delete()
            .eq("id", note_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        logger.info("Note deleted", note_id=note_id, user_id=current_user["id"])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete note", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
