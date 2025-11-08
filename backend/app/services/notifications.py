"""
Notification Service
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.core.supabase import supabase_client
import structlog

logger = structlog.get_logger()


class NotificationService:
    """Service for managing notifications and reminders"""

    def __init__(self, user_id: str):
        self.user_id = user_id

    async def create_task_reminder(
        self, task_id: str, scheduled_start: datetime, reminder_minutes_before: int = 15
    ) -> Dict[str, Any]:
        """
        Create a reminder notification for a task
        """
        try:
            scheduled_for = scheduled_start - timedelta(minutes=reminder_minutes_before)

            notification_data = {
                "user_id": self.user_id,
                "task_id": task_id,
                "type": "reminder",
                "title": "Task Reminder",
                "message": f"Your task starts in {reminder_minutes_before} minutes",
                "scheduled_for": scheduled_for.isoformat(),
                "channels": ["in_app", "push"],
                "created_at": datetime.utcnow().isoformat(),
            }

            response = (
                supabase_client.table("notifications").insert(notification_data).execute()
            )

            logger.info(
                "Reminder created",
                user_id=self.user_id,
                task_id=task_id,
                scheduled_for=scheduled_for,
            )

            return response.data[0]
        except Exception as e:
            logger.error("Failed to create reminder", error=str(e))
            raise

    async def create_deadline_notification(
        self, task_id: str, deadline: datetime
    ) -> Dict[str, Any]:
        """
        Create a deadline notification for a task
        """
        try:
            notification_data = {
                "user_id": self.user_id,
                "task_id": task_id,
                "type": "deadline",
                "title": "Task Deadline",
                "message": "Your task deadline is approaching",
                "scheduled_for": deadline.isoformat(),
                "channels": ["in_app", "email"],
                "created_at": datetime.utcnow().isoformat(),
            }

            response = (
                supabase_client.table("notifications").insert(notification_data).execute()
            )

            logger.info(
                "Deadline notification created",
                user_id=self.user_id,
                task_id=task_id,
            )

            return response.data[0]
        except Exception as e:
            logger.error("Failed to create deadline notification", error=str(e))
            raise

    async def send_nudge(self, task_id: str, message: str) -> Dict[str, Any]:
        """
        Send a nudge notification to encourage task completion
        """
        try:
            notification_data = {
                "user_id": self.user_id,
                "task_id": task_id,
                "type": "nudge",
                "title": "Task Nudge",
                "message": message,
                "scheduled_for": datetime.utcnow().isoformat(),
                "channels": ["in_app"],
                "created_at": datetime.utcnow().isoformat(),
            }

            response = (
                supabase_client.table("notifications").insert(notification_data).execute()
            )

            # Immediately mark as sent since it's instant
            await self._mark_as_sent(response.data[0]["id"])

            logger.info("Nudge sent", user_id=self.user_id, task_id=task_id)

            return response.data[0]
        except Exception as e:
            logger.error("Failed to send nudge", error=str(e))
            raise

    async def get_pending_notifications(self) -> List[Dict]:
        """
        Get user's pending notifications
        """
        try:
            response = (
                supabase_client.table("notifications")
                .select("*")
                .eq("user_id", self.user_id)
                .is_("sent_at", "null")
                .lte("scheduled_for", datetime.utcnow().isoformat())
                .order("scheduled_for")
                .execute()
            )

            return response.data
        except Exception as e:
            logger.error("Failed to get pending notifications", error=str(e))
            return []

    async def get_unread_notifications(self) -> List[Dict]:
        """
        Get user's unread notifications
        """
        try:
            response = (
                supabase_client.table("notifications")
                .select("*")
                .eq("user_id", self.user_id)
                .is_("read_at", "null")
                .not_.is_("sent_at", "null")
                .order("sent_at", desc=True)
                .limit(50)
                .execute()
            )

            return response.data
        except Exception as e:
            logger.error("Failed to get unread notifications", error=str(e))
            return []

    async def mark_as_read(self, notification_id: str) -> None:
        """
        Mark a notification as read
        """
        try:
            supabase_client.table("notifications").update(
                {"read_at": datetime.utcnow().isoformat()}
            ).eq("id", notification_id).eq("user_id", self.user_id).execute()

            logger.info("Notification marked as read", notification_id=notification_id)
        except Exception as e:
            logger.error("Failed to mark notification as read", error=str(e))
            raise

    async def _mark_as_sent(self, notification_id: str) -> None:
        """
        Mark a notification as sent (internal use)
        """
        try:
            supabase_client.table("notifications").update(
                {"sent_at": datetime.utcnow().isoformat()}
            ).eq("id", notification_id).execute()
        except Exception as e:
            logger.error("Failed to mark notification as sent", error=str(e))

    async def process_scheduled_notifications(self) -> int:
        """
        Process and send all pending notifications (to be called by a scheduled job)
        """
        try:
            pending = await self.get_pending_notifications()

            sent_count = 0
            for notification in pending:
                # TODO: Implement actual notification sending (email, push, etc.)
                # For now, just mark as sent
                await self._mark_as_sent(notification["id"])
                sent_count += 1

            logger.info(
                "Scheduled notifications processed",
                user_id=self.user_id,
                sent_count=sent_count,
            )

            return sent_count
        except Exception as e:
            logger.error("Failed to process scheduled notifications", error=str(e))
            return 0

    async def create_schedule_reminders_for_tasks(
        self, scheduled_tasks: List[Dict]
    ) -> List[Dict]:
        """
        Create reminders for a list of scheduled tasks
        """
        created_reminders = []

        # Get user preferences for reminder settings
        prefs_response = (
            supabase_client.table("user_preferences")
            .select("*")
            .eq("user_id", self.user_id)
            .execute()
        )

        reminder_minutes = [15]  # Default
        if prefs_response.data:
            notification_settings = prefs_response.data[0].get(
                "notification_settings", {}
            )
            reminder_minutes = notification_settings.get(
                "reminder_minutes_before", [15]
            )

        for task in scheduled_tasks:
            if task.get("scheduled_start"):
                scheduled_start = datetime.fromisoformat(task["scheduled_start"])

                for minutes_before in reminder_minutes:
                    try:
                        reminder = await self.create_task_reminder(
                            task["id"], scheduled_start, minutes_before
                        )
                        created_reminders.append(reminder)
                    except Exception as e:
                        logger.error(
                            "Failed to create reminder for task",
                            task_id=task["id"],
                            error=str(e),
                        )

        return created_reminders
