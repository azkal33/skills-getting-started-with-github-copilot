"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""


def test_unregister_successful_removes_participant(client):
    """
    Arrange: Existing participant in activity
    Act: DELETE unregister request
    Assert: Participant is removed, response confirms
    """
    from src import app
    
    # Arrange
    activity_name = "Chess Club"
    participant_to_remove = app.activities[activity_name]["participants"][0]
    original_count = len(app.activities[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={participant_to_remove}"
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert participant_to_remove not in app.activities[activity_name]["participants"]
    assert len(app.activities[activity_name]["participants"]) == original_count - 1


def test_unregister_nonexistent_activity_returns_404(client):
    """
    Arrange: Non-existent activity name
    Act: DELETE unregister request for non-existent activity
    Assert: Returns 404 Activity not found
    """
    # Arrange
    test_email = "student@mergington.edu"
    nonexistent_activity = "Nonexistent Club"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/unregister?email={test_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_non_registered_participant_returns_404(client):
    """
    Arrange: Email not in activity participants list
    Act: DELETE unregister request for non-registered participant
    Assert: Returns 404 Participant not found
    """
    # Arrange
    activity_name = "Chess Club"
    unregistered_email = "nonexistent@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={unregistered_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_removes_only_from_target_activity(client):
    """
    Arrange: Participant in activity
    Act: DELETE unregister from one activity
    Assert: Removed from target activity only
    """
    from src import app
    
    # Arrange
    activity_name = "Programming Class"
    participant = app.activities[activity_name]["participants"][0]
    other_activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={participant}"
    )
    
    # Assert
    assert response.status_code == 200
    assert participant not in app.activities[activity_name]["participants"]
    # Verify other activities are unaffected
