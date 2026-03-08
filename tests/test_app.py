import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset participants for each activity before each test
    for activity in activities.values():
        if "participants" in activity:
            activity["participants"] = []


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert "Signed up test@mergington.edu for Chess Club" in response.json()["message"]
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_for_activity():
    # Add participant first
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    # Unregister endpoint must exist in app.py for this test to pass
    response = client.post("/activities/Chess Club/unregister?email=test@mergington.edu")
    assert response.status_code == 200
    assert "test@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_signed_up():
    response = client.post("/activities/Chess Club/unregister?email=test@mergington.edu")
    assert response.status_code == 400
    assert "Student not signed up" in response.json()["detail"]
