"""Tests for GET /activities endpoint using AAA pattern"""


def test_get_activities_returns_all_activities(client):
    """
    Arrange: Client is ready
    Act: Make GET request to /activities
    Assert: Response contains all activities with correct structure
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    assert "Chess Club" in activities
    assert "Programming Class" in activities


def test_get_activities_activity_has_required_fields(client):
    """
    Arrange: Client is ready
    Act: Make GET request to /activities
    Assert: Each activity has required fields
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participants_are_emails(client):
    """
    Arrange: Client is ready
    Act: Make GET request to /activities
    Assert: Participants list contains valid email strings
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation
