"""
Task Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.models.task import Task, TaskCreate, TaskUpdate
from app.api.dependencies import get_current_user
from app.core.supabase import supabase_client
import structlog
from datetime import datetime

router = APIRouter()
logger = structlog.get_logger()


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    """Create a new task"""
    try:
        task_data = task.model_dump()
        task_data["user_id"] = current_user["id"]
        task_data["created_at"] = datetime.utcnow().isoformat()
        task_data["updated_at"] = datetime.utcnow().isoformat()

        response = supabase_client.table("tasks").insert(task_data).execute()

        logger.info("Task created", task_id=response.data[0]["id"], user_id=current_user["id"])
        return Task(**response.data[0])
    except Exception as e:
        logger.error("Failed to create task", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[Task])
async def list_tasks(
    current_user: dict = Depends(get_current_user),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
):
    """List user's tasks with optional filters"""
    try:
        query = supabase_client.table("tasks").select("*").eq("user_id", current_user["id"])

        if status:
            query = query.eq("status", status)
        if priority:
            query = query.eq("priority", priority)

        response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()

        return [Task(**task) for task in response.data]
    except Exception as e:
        logger.error("Failed to list tasks", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific task"""
    try:
        response = (
            supabase_client.table("tasks")
            .select("*")
            .eq("id", task_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        return Task(**response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get task", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{task_id}", response_model=Task)
async def update_task(
    task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user)
):
    """Update a task"""
    try:
        update_data = task_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()

        response = (
            supabase_client.table("tasks")
            .update(update_data)
            .eq("id", task_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        logger.info("Task updated", task_id=task_id, user_id=current_user["id"])
        return Task(**response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update task", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a task"""
    try:
        response = (
            supabase_client.table("tasks")
            .delete()
            .eq("id", task_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        logger.info("Task deleted", task_id=task_id, user_id=current_user["id"])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete task", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
