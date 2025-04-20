import sys
from pathlib import Path

# Add autogen to PYTHONPATH dynamically
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "autogen"))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import UUID
import time


client = TestClient(app)

def test_assistant_flow():
    # Step 1: Register a new user
    register_response = client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "securepassword",
        "name": "Test User"
    })
    assert register_response.status_code == 200
    assert "access_token" in register_response.json()
    token = register_response.json()["access_token"]

    # Step 2: Get user profile to extract user_id
    profile_response = client.get("/api/v1/user/profile", headers={
        "Authorization": f"Bearer {token}"
    })
    assert profile_response.status_code == 200
    user_id = profile_response.json()["id"]
    assert UUID(user_id)  # Validates UUID format

    # Step 3: Send a message to the assistant
    message = "Hello, I need help planning my family's week."
    assistant_response = client.post("/api/v1/assistant/message", json={
        "message": message
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    assert assistant_response.status_code == 200
    assert "response" in assistant_response.json()
    assert len(assistant_response.json()["response"]) > 0

    # Step 4: (Optional) Sleep briefly to allow async Cosmos write
    time.sleep(1)

    # Step 5: (Pending) Optionally validate Cosmos interaction via DB-level checks
    # Requires mocking or exposing Cosmos validation endpoint (not included here)
