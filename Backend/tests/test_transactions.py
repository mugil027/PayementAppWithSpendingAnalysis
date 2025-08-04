# File: Backend/tests/test_transactions.py
# Description: Tests for the transaction-related endpoints.

from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient) -> dict:
    """Helper function to get authentication headers."""
    login_response = client.post(
        "/token",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_transaction(client: TestClient):
    """
    Test creating a transaction for the logged-in user.
    """
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/transactions/",
        headers=headers,
        json={"amount": 99.99, "category": "Shopping", "description": "New headphones"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 99.99
    assert data["category"] == "Shopping"

def test_create_transaction_unauthenticated(client: TestClient):
    """
    Test that creating a transaction fails without authentication.
    """
    response = client.post(
        "/api/v1/transactions/",
        json={"amount": 50.00, "category": "Food"},
    )
    assert response.status_code == 401 # Unauthorized

def test_read_transactions(client: TestClient):
    """
    Test reading transactions for the logged-in user.
    """
    headers = get_auth_headers(client)
    response = client.get("/api/v1/transactions/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check if the transaction created earlier is in the list
    assert any(item["description"] == "New headphones" for item in data)
