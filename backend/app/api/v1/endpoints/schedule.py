"""
Schedule Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from pydantic import BaseModel
from app.api.dependencies import get_current_user
from app.services.ai_scheduler import AIScheduler
import structlog
from datetime import date, datetime

router = APIRouter()
logger = structlog.get_logger()


class GenerateScheduleRequest(BaseModel):
    date: date
    force_regenerate: bool = False


class ScheduleResponse(BaseModel):
    id: str
    user_id: str
    date: date
    tasks: List[dict]
    metadata: dict
    created_at: datetime


@router.post("/generate", response_model=ScheduleResponse)
async def generate_schedule(
    request: GenerateScheduleRequest, current_user: dict = Depends(get_current_user)
):
    """Generate AI-powered schedule for a specific date"""
    try:
        scheduler = AIScheduler(current_user["id"])
        schedule = await scheduler.generate_schedule(
            request.date, force_regenerate=request.force_regenerate
        )

        logger.info(
            "Schedule generated",
            user_id=current_user["id"],
            date=str(request.date),
        )
        return schedule
    except Exception as e:
        logger.error("Failed to generate schedule", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{date}", response_model=ScheduleResponse)
async def get_schedule(date: str, current_user: dict = Depends(get_current_user)):
    """Get schedule for a specific date"""
    try:
        scheduler = AIScheduler(current_user["id"])
        schedule = await scheduler.get_schedule(date)

        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No schedule found for {date}",
            )

        return schedule
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get schedule", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{schedule_id}/adjust")
async def adjust_schedule(
    schedule_id: str, adjustments: dict, current_user: dict = Depends(get_current_user)
):
    """Manually adjust a generated schedule"""
    try:
        scheduler = AIScheduler(current_user["id"])
        updated_schedule = await scheduler.adjust_schedule(schedule_id, adjustments)

        logger.info("Schedule adjusted", schedule_id=schedule_id, user_id=current_user["id"])
        return updated_schedule
    except Exception as e:
        logger.error("Failed to adjust schedule", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
