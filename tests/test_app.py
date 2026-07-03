import urllib.parse


def test_get_activities(client):
    # Arrange: client fixture provided

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "new.student@example.edu"
    enc_activity = urllib.parse.quote(activity, safe="")
    enc_email = urllib.parse.quote(email, safe="")

    # Act
    resp = client.post(f"/activities/{enc_activity}/signup?email={enc_email}")

    # Assert
    assert resp.status_code == 200
    payload = resp.json()
    assert email in payload.get("message", "")
    # Confirm in-memory state
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_remove_participant(client):
    # Arrange
    activity = "Chess Club"
    # Use an existing participant from seed data
    email = "michael@mergington.edu"
    enc_activity = urllib.parse.quote(activity, safe="")
    enc_email = urllib.parse.quote(email, safe="")

    # Act
    resp = client.delete(f"/activities/{enc_activity}/participants?email={enc_email}")

    # Assert
    assert resp.status_code == 200
    payload = resp.json()
    assert email in payload.get("message", "")
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
