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
    # Arrange
    # (No setup needed for this test)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity():
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    assert email in activities[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_for_activity():
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{invalid_activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_signed_up():
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    assert "Student not signed up" in response.json()["detail"]
