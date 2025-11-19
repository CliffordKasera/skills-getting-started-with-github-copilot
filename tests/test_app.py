import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to /static/index.html
    assert str(response.url).endswith("/static/index.html") or response.history

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success():
    email = "teststudent@mergington.edu"
    activity = "Science Club"
    # Remove if already present (directly modify the in-memory DB)
    from src.app import activities
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_already_signed_up():
    email = "emma@mergington.edu"
    activity = "Programming Class"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_activity_not_found():
    email = "ghost@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
