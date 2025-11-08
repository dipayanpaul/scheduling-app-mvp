"""
Tests for Task API Endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task_unauthorized(client: TestClient):
    """Test creating a task without authentication"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
        },
    )
    assert response.status_code == 403  # No auth provided


# Note: Full integration tests would require mocking Supabase
# These are example test structures

@pytest.mark.skip(reason="Requires Supabase mock")
def test_create_task_success(client: TestClient, auth_headers: dict):
    """Test creating a task successfully"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "estimated_duration": 60,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"


@pytest.mark.skip(reason="Requires Supabase mock")
def test_list_tasks(client: TestClient, auth_headers: dict):
    """Test listing tasks"""
    response = client.get("/api/v1/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.skip(reason="Requires Supabase mock")
def test_update_task(client: TestClient, auth_headers: dict):
    """Test updating a task"""
    task_id = "test-task-id"
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "completed"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


@pytest.mark.skip(reason="Requires Supabase mock")
def test_delete_task(client: TestClient, auth_headers: dict):
    """Test deleting a task"""
    task_id = "test-task-id"
    response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204
