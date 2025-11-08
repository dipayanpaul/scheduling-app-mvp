"""
Pytest Configuration and Fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_user():
    """Mock user for testing"""
    return {
        "id": "test-user-id",
        "email": "test@example.com",
        "user_metadata": {"full_name": "Test User"},
    }


@pytest.fixture
def auth_headers(mock_user):
    """Mock authentication headers"""
    return {"Authorization": "Bearer mock-token"}
