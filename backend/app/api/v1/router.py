"""
API v1 Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import tasks, notes, schedule, auth, users, ingestion

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(notes.router, prefix="/notes", tags=["Notes"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion"])
