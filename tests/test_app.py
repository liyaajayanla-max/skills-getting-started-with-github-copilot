def test_get_activities_success(client):
    # Arrange: No specific setup needed as data is reset in fixture
    
    # Act: Make GET request to /activities
    response = client.get("/activities")
    
    # Assert: Check status code and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert len(data["Chess Club"]["participants"]) == 2  # Original count

def test_signup_success(client):
    # Arrange: Use a new email not already signed up
    
    # Act: Make POST request to signup
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    
    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up newstudent@mergington.edu for Chess Club" == data["message"]
    # Verify added to participants
    activities_response = client.get("/activities")
    assert "newstudent@mergington.edu" in activities_response.json()["Chess Club"]["participants"]

def test_signup_activity_not_found(client):
    # Arrange: Use a non-existent activity name
    
    # Act: Make POST request
    response = client.post("/activities/NonExistent Activity/signup", params={"email": "test@mergington.edu"})
    
    # Assert: Check 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" == data["detail"]

def test_signup_already_signed_up(client):
    # Arrange: Sign up first
    client.post("/activities/Chess Club/signup", params={"email": "duplicate@mergington.edu"})
    
    # Act: Try to sign up again
    response = client.post("/activities/Chess Club/signup", params={"email": "duplicate@mergington.edu"})
    
    # Assert: Check 400 error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is already signed up" == data["detail"]

def test_delete_signup_success(client):
    # Arrange: Sign up first
    client.post("/activities/Chess Club/signup", params={"email": "removeme@mergington.edu"})
    
    # Act: Make DELETE request
    response = client.delete("/activities/Chess Club/signup", params={"email": "removeme@mergington.edu"})
    
    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Removed removeme@mergington.edu from Chess Club" == data["message"]
    # Verify removed from participants
    activities_response = client.get("/activities")
    assert "removeme@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]

def test_delete_signup_activity_not_found(client):
    # Arrange: Use a non-existent activity name
    
    # Act: Make DELETE request
    response = client.delete("/activities/NonExistent Activity/signup", params={"email": "test@mergington.edu"})
    
    # Assert: Check 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" == data["detail"]

def test_delete_signup_not_signed_up(client):
    # Arrange: Use an email not signed up for the activity
    
    # Act: Make DELETE request
    response = client.delete("/activities/Chess Club/signup", params={"email": "notsigned@mergington.edu"})
    
    # Assert: Check 400 error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up" == data["detail"]