from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant():
    response = client.post("/activities/Chess%20Club/signup?email=teststudent@mergington.edu")

    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "Signed up teststudent@mergington.edu for Chess Club"

    get_response = client.get("/activities")
    assert get_response.status_code == 200
    activity = get_response.json()["Chess Club"]
    assert "teststudent@mergington.edu" in activity["participants"]


def test_signup_duplicate_returns_400():
    email = "duplicate@mergington.edu"
    client.post(f"/activities/Programming%20Class/signup?email={email}")

    response = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_from_activity():
    email = "removeme@mergington.edu"
    client.post(f"/activities/Gym%20Class/signup?email={email}")

    delete_response = client.delete(f"/activities/Gym%20Class/participants?email={email}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from Gym Class"

    get_response = client.get("/activities")
    activity = get_response.json()["Gym Class"]
    assert email not in activity["participants"]
