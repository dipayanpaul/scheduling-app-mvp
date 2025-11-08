"""
AI-Powered Scheduling Service
"""
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
from app.services.llm_provider import LLMService, Message
from app.core.supabase import supabase_client
import structlog
import json

logger = structlog.get_logger()


class AIScheduler:
    """AI-powered task scheduling service"""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.llm_service = LLMService()

    async def generate_schedule(
        self, target_date: date, force_regenerate: bool = False
    ) -> Dict[str, Any]:
        """Generate an AI-powered schedule for a specific date"""
        try:
            # Check if schedule already exists
            if not force_regenerate:
                existing_schedule = await self.get_schedule(str(target_date))
                if existing_schedule:
                    return existing_schedule

            # Get user preferences
            prefs_response = (
                supabase_client.table("user_preferences")
                .select("*")
                .eq("user_id", self.user_id)
                .execute()
            )
            preferences = prefs_response.data[0] if prefs_response.data else {}

            # Get pending tasks
            tasks_response = (
                supabase_client.table("tasks")
                .select("*")
                .eq("user_id", self.user_id)
                .in_("status", ["pending", "in_progress"])
                .execute()
            )
            tasks = tasks_response.data

            if not tasks:
                return {
                    "message": "No pending tasks to schedule",
                    "date": target_date,
                    "tasks": [],
                }

            # Generate schedule using LLM
            scheduled_tasks = await self._generate_schedule_with_llm(
                tasks, preferences, target_date
            )

            # Save schedule to database
            schedule_data = {
                "user_id": self.user_id,
                "date": str(target_date),
                "tasks": scheduled_tasks,
                "metadata": {
                    "ai_generated": True,
                    "adjustments_count": 0,
                    "task_count": len(scheduled_tasks),
                },
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            schedule_response = (
                supabase_client.table("schedules").insert(schedule_data).execute()
            )

            logger.info(
                "Schedule generated",
                user_id=self.user_id,
                date=str(target_date),
                task_count=len(scheduled_tasks),
            )

            return schedule_response.data[0]
        except Exception as e:
            logger.error("Failed to generate schedule", error=str(e))
            raise

    async def _generate_schedule_with_llm(
        self, tasks: List[Dict], preferences: Dict, target_date: date
    ) -> List[Dict]:
        """Use LLM to generate optimized schedule"""
        # Prepare context for LLM
        work_start = preferences.get("work_hours_start", "09:00")
        work_end = preferences.get("work_hours_end", "17:00")
        break_duration = preferences.get("preferred_break_duration", 15)

        tasks_context = json.dumps(
            [
                {
                    "id": task["id"],
                    "title": task["title"],
                    "description": task.get("description", ""),
                    "priority": task.get("priority", "medium"),
                    "estimated_duration": task.get("estimated_duration", 60),
                }
                for task in tasks
            ],
            indent=2,
        )

        prompt = f"""You are an AI scheduling assistant. Generate an optimized schedule for the following tasks on {target_date}.

User preferences:
- Work hours: {work_start} to {work_end}
- Preferred break duration: {break_duration} minutes

Tasks to schedule:
{tasks_context}

Consider:
1. Task priorities (urgent > high > medium > low)
2. Estimated durations
3. User's work hours
4. Include breaks between tasks
5. Group similar tasks when possible
6. Start with high-priority items

Return ONLY a JSON array with this structure:
[
  {{
    "task_id": "task_id_here",
    "start_time": "HH:MM",
    "end_time": "HH:MM",
    "order": 1
  }}
]"""

        messages = [Message(role="user", content=prompt)]

        response = await self.llm_service.generate(
            messages=messages, temperature=0.3, max_tokens=2000
        )

        # Parse LLM response
        try:
            # Extract JSON from response (in case there's extra text)
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            json_str = response[json_start:json_end]
            scheduled_tasks = json.loads(json_str)

            # Enrich with task details
            task_map = {task["id"]: task for task in tasks}
            for scheduled_task in scheduled_tasks:
                task_id = scheduled_task["task_id"]
                if task_id in task_map:
                    scheduled_task["task"] = task_map[task_id]

            return scheduled_tasks
        except json.JSONDecodeError as e:
            logger.error("Failed to parse LLM response", error=str(e), response=response)
            # Fallback: create simple schedule
            return self._create_fallback_schedule(tasks, work_start)

    def _create_fallback_schedule(
        self, tasks: List[Dict], start_time: str
    ) -> List[Dict]:
        """Create a simple fallback schedule if LLM fails"""
        scheduled_tasks = []
        current_time = datetime.strptime(start_time, "%H:%M")

        # Sort by priority
        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
        sorted_tasks = sorted(
            tasks, key=lambda t: priority_order.get(t.get("priority", "medium"), 2)
        )

        for i, task in enumerate(sorted_tasks[:10]):  # Limit to 10 tasks
            duration = task.get("estimated_duration", 60)
            end_time = current_time + timedelta(minutes=duration)

            scheduled_tasks.append(
                {
                    "task_id": task["id"],
                    "task": task,
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": end_time.strftime("%H:%M"),
                    "order": i + 1,
                }
            )

            current_time = end_time + timedelta(minutes=15)  # 15 min break

        return scheduled_tasks

    async def get_schedule(self, date: str) -> Optional[Dict]:
        """Get existing schedule for a date"""
        try:
            response = (
                supabase_client.table("schedules")
                .select("*")
                .eq("user_id", self.user_id)
                .eq("date", date)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            return response.data[0] if response.data else None
        except Exception as e:
            logger.error("Failed to get schedule", error=str(e))
            return None

    async def adjust_schedule(
        self, schedule_id: str, adjustments: Dict
    ) -> Dict[str, Any]:
        """Manually adjust a generated schedule"""
        try:
            # Get existing schedule
            schedule_response = (
                supabase_client.table("schedules")
                .select("*")
                .eq("id", schedule_id)
                .eq("user_id", self.user_id)
                .execute()
            )

            if not schedule_response.data:
                raise ValueError("Schedule not found")

            schedule = schedule_response.data[0]
            metadata = schedule.get("metadata", {})
            metadata["adjustments_count"] = metadata.get("adjustments_count", 0) + 1

            # Update schedule
            update_data = {
                "tasks": adjustments.get("tasks", schedule["tasks"]),
                "metadata": metadata,
                "updated_at": datetime.utcnow().isoformat(),
            }

            updated_response = (
                supabase_client.table("schedules")
                .update(update_data)
                .eq("id", schedule_id)
                .execute()
            )

            logger.info("Schedule adjusted", schedule_id=schedule_id, user_id=self.user_id)

            return updated_response.data[0]
        except Exception as e:
            logger.error("Failed to adjust schedule", error=str(e))
            raise
