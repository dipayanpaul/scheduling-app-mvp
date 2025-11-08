"""
User and Preferences Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserPreferences, UserPreferencesUpdate
from app.api.dependencies import get_current_user
from app.core.supabase import supabase_client
import structlog
from datetime import datetime

router = APIRouter()
logger = structlog.get_logger()


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/preferences", response_model=UserPreferences)
async def get_user_preferences(current_user: dict = Depends(get_current_user)):
    """Get user preferences"""
    try:
        response = (
            supabase_client.table("user_preferences")
            .select("*")
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            # Create default preferences
            default_prefs = {
                "user_id": current_user["id"],
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            response = (
                supabase_client.table("user_preferences").insert(default_prefs).execute()
            )

        return UserPreferences(**response.data[0])
    except Exception as e:
        logger.error("Failed to get user preferences", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/preferences", response_model=UserPreferences)
async def update_user_preferences(
    preferences: UserPreferencesUpdate, current_user: dict = Depends(get_current_user)
):
    """Update user preferences"""
    try:
        update_data = preferences.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()

        response = (
            supabase_client.table("user_preferences")
            .update(update_data)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User preferences not found",
            )

        logger.info("User preferences updated", user_id=current_user["id"])
        return UserPreferences(**response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update user preferences", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
