import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400


def test_unregister_participant():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Unregister
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert "Successfully unregistered" in response.json()["message"]
    # Try again (should fail)
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
