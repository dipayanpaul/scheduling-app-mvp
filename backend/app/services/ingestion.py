"""
Multimodal Ingestion Service
"""
from typing import Dict, Any, Optional
from fastapi import UploadFile
from app.services.llm_provider import LLMService, Message
from app.core.supabase import supabase_client
from app.core.config import settings
import structlog
import json
import uuid
import aiofiles
import os
from datetime import datetime

logger = structlog.get_logger()


class IngestionService:
    """Service for processing multimodal input (text, voice, images)"""

    def __init__(self):
        self.llm_service = LLMService()

    async def process_text(
        self, user_id: str, content: str, title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process text input and extract tasks"""
        try:
            # Extract tasks using LLM
            extracted_tasks = await self._extract_tasks_from_text(content)

            # Save note
            note_data = {
                "user_id": user_id,
                "title": title,
                "content": content,
                "source_type": "text",
                "extracted_tasks": extracted_tasks,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            note_response = supabase_client.table("notes").insert(note_data).execute()

            # Create tasks if extracted
            created_tasks = []
            if extracted_tasks:
                created_tasks = await self._create_tasks_from_extraction(
                    user_id, extracted_tasks
                )

            logger.info(
                "Text processed",
                user_id=user_id,
                extracted_count=len(extracted_tasks),
            )

            return {
                "note_id": note_response.data[0]["id"],
                "extracted_tasks": extracted_tasks,
                "created_tasks": created_tasks,
                "status": "completed",
            }
        except Exception as e:
            logger.error("Failed to process text", error=str(e))
            raise

    async def process_voice(
        self, user_id: str, audio_file: UploadFile
    ) -> Dict[str, Any]:
        """Process voice recording and extract tasks"""
        try:
            # Save audio file
            file_path = await self._save_upload_file(audio_file)

            # TODO: Implement actual speech-to-text
            # For now, create a placeholder transcription
            transcription = f"[Audio transcription would go here for {audio_file.filename}]"

            # Extract tasks from transcription
            extracted_tasks = await self._extract_tasks_from_text(transcription)

            # Save note
            note_data = {
                "user_id": user_id,
                "content": transcription,
                "source_type": "voice",
                "media_url": file_path,
                "transcription": transcription,
                "extracted_tasks": extracted_tasks,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            note_response = supabase_client.table("notes").insert(note_data).execute()

            # Create tasks
            created_tasks = await self._create_tasks_from_extraction(
                user_id, extracted_tasks
            )

            logger.info("Voice processed", user_id=user_id)

            return {
                "note_id": note_response.data[0]["id"],
                "transcription": transcription,
                "extracted_tasks": extracted_tasks,
                "created_tasks": created_tasks,
                "status": "completed",
            }
        except Exception as e:
            logger.error("Failed to process voice", error=str(e))
            raise

    async def process_image(
        self, user_id: str, image_file: UploadFile
    ) -> Dict[str, Any]:
        """Process image and extract tasks"""
        try:
            # Save image file
            file_path = await self._save_upload_file(image_file)

            # TODO: Implement actual OCR/image analysis
            # For now, create a placeholder
            extracted_text = f"[Image text extraction would go here for {image_file.filename}]"

            # Extract tasks
            extracted_tasks = await self._extract_tasks_from_text(extracted_text)

            # Save note
            note_data = {
                "user_id": user_id,
                "content": extracted_text,
                "source_type": "image",
                "media_url": file_path,
                "extracted_tasks": extracted_tasks,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            note_response = supabase_client.table("notes").insert(note_data).execute()

            # Create tasks
            created_tasks = await self._create_tasks_from_extraction(
                user_id, extracted_tasks
            )

            logger.info("Image processed", user_id=user_id)

            return {
                "note_id": note_response.data[0]["id"],
                "extracted_text": extracted_text,
                "extracted_tasks": extracted_tasks,
                "created_tasks": created_tasks,
                "status": "completed",
            }
        except Exception as e:
            logger.error("Failed to process image", error=str(e))
            raise

    async def _extract_tasks_from_text(self, text: str) -> list:
        """Use LLM to extract actionable tasks from text"""
        prompt = f"""Extract actionable tasks from the following text. Identify task titles, descriptions, priorities, and estimated durations.

Text:
{text}

Return ONLY a JSON array with this structure:
[
  {{
    "title": "Task title",
    "description": "Optional description",
    "priority": "low|medium|high|urgent",
    "estimated_duration": 60
  }}
]

If no clear tasks are found, return an empty array: []"""

        messages = [Message(role="user", content=prompt)]

        response = await self.llm_service.generate(
            messages=messages, temperature=0.2, max_tokens=1500
        )

        try:
            # Extract JSON from response
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            json_str = response[json_start:json_end]
            tasks = json.loads(json_str)
            return tasks
        except json.JSONDecodeError as e:
            logger.error("Failed to parse task extraction", error=str(e))
            return []

    async def _create_tasks_from_extraction(
        self, user_id: str, extracted_tasks: list
    ) -> list:
        """Create task records from extracted task data"""
        created_tasks = []

        for task_data in extracted_tasks:
            task_record = {
                "user_id": user_id,
                "title": task_data["title"],
                "description": task_data.get("description"),
                "priority": task_data.get("priority", "medium"),
                "estimated_duration": task_data.get("estimated_duration"),
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            response = supabase_client.table("tasks").insert(task_record).execute()
            created_tasks.append(response.data[0])

        return created_tasks

    async def _save_upload_file(self, upload_file: UploadFile) -> str:
        """Save uploaded file to storage"""
        try:
            # Generate unique filename
            file_extension = os.path.splitext(upload_file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

            # Save file
            async with aiofiles.open(file_path, "wb") as f:
                content = await upload_file.read()
                await f.write(content)

            logger.info("File saved", path=file_path)
            return file_path
        except Exception as e:
            logger.error("Failed to save upload file", error=str(e))
            raise

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of an ingestion job"""
        # Placeholder for async job tracking
        return {"job_id": job_id, "status": "completed"}
