# File: Backend/tests/test_auth.py
# Description: Tests for user creation and authentication endpoints.

from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    """
    Test creating a new user successfully.
    """
    response = client.post(
        "/api/v1/users/",
        json={"email": "testuser@example.com", "full_name": "Test User", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data # Ensure password is not returned

def test_login_for_access_token(client: TestClient):
    """
    Test logging in to get an access token.
    This test depends on the user created in test_create_user.
    """
    response = client.post(
        "/token",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_user_me(client: TestClient):
    """
    Test accessing a protected route (/users/me) with a valid token.
    """
    # First, log in to get a token
    login_response = client.post(
        "/token",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    token = login_response.json()["access_token"]
    
    # Now, access the protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
