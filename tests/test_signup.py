"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""
import pytest


def test_signup_successful_adds_participant(client):
    """
    Arrange: Fresh activities data, test email, activity name
    Act: POST signup request
    Assert: Participant is added, response confirms
    """
    from src import app
    
    # Arrange
    test_email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    original_count = len(app.activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert test_email in app.activities[activity_name]["participants"]
    assert len(app.activities[activity_name]["participants"]) == original_count + 1


def test_signup_nonexistent_activity_returns_404(client):
    """
    Arrange: Non-existent activity name, test email
    Act: POST signup request for non-existent activity
    Assert: Returns 404 Activity not found
    """
    # Arrange
    test_email = "student@mergington.edu"
    nonexistent_activity = "Nonexistent Club"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_registration_returns_400(client):
    """
    Arrange: Already registered student, activity with that participant
    Act: POST signup request with same email
    Assert: Returns 400 Already signed up
    """
    from src import app
    
    # Arrange
    activity_name = "Chess Club"
    already_registered_email = app.activities[activity_name]["participants"][0]
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={already_registered_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_adds_email_to_correct_activity(client):
    """
    Arrange: Multiple activities, test email
    Act: POST signup for specific activity
    Assert: Email added to correct activity only
    """
    from src import app
    
    # Arrange
    test_email = "specific@mergington.edu"
    target_activity = "Programming Class"
    other_activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{target_activity}/signup?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert test_email in app.activities[target_activity]["participants"]
    assert test_email not in app.activities[other_activity]["participants"]
