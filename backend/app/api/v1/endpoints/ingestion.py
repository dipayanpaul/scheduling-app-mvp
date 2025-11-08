"""
Multimodal Ingestion Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import Optional
from app.api.dependencies import get_current_user
from app.services.ingestion import IngestionService
from app.models.note import SourceType
import structlog

router = APIRouter()
logger = structlog.get_logger()
ingestion_service = IngestionService()


@router.post("/text")
async def ingest_text(
    content: str = Form(...),
    title: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user),
):
    """Process text input and extract tasks"""
    try:
        result = await ingestion_service.process_text(
            user_id=current_user["id"], content=content, title=title
        )

        logger.info("Text ingested", user_id=current_user["id"])
        return result
    except Exception as e:
        logger.error("Failed to ingest text", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/voice")
async def ingest_voice(
    file: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    """Process voice recording and extract tasks"""
    try:
        result = await ingestion_service.process_voice(
            user_id=current_user["id"], audio_file=file
        )

        logger.info("Voice ingested", user_id=current_user["id"])
        return result
    except Exception as e:
        logger.error("Failed to ingest voice", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/image")
async def ingest_image(
    file: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    """Process image and extract tasks"""
    try:
        result = await ingestion_service.process_image(
            user_id=current_user["id"], image_file=file
        )

        logger.info("Image ingested", user_id=current_user["id"])
        return result
    except Exception as e:
        logger.error("Failed to ingest image", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/status/{job_id}")
async def get_ingestion_status(
    job_id: str, current_user: dict = Depends(get_current_user)
):
    """Get status of an ingestion job"""
    try:
        status = await ingestion_service.get_job_status(job_id)
        return status
    except Exception as e:
        logger.error("Failed to get ingestion status", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
