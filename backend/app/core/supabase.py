"""
Supabase Client Configuration
"""
from supabase import create_client, Client
from app.core.config import settings
import structlog

logger = structlog.get_logger()


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance
    """
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return supabase
    except Exception as e:
        logger.error("Failed to create Supabase client", error=str(e))
        raise


# Global client instance
supabase_client = get_supabase_client()
