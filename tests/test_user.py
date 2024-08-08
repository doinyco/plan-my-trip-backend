# tests/test_user.py
import pytest
from app import create_app, db
from app.models.user import User


def test_create_user(client):
    # Arrange
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Testpassword123"
    }

    # Act
    response = client.post("/auth/register", json=data)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.get_json()}")

    # Assert
    assert response.status_code == 200
    response_data = response.get_json()
    assert "success" in response_data
    assert response_data["success"] == "Registration successful. You can now log in."


def test_create_user_invalid_data(client):
    # Arrange
    data = {
        "username": "testuser"
        # missing email or other required fields
    }

    # Act
    response = client.post("/auth/register", json=data)

    # Assert
    assert response.status_code == 400
    response_data = response.get_json()
    assert "error" in response_data
    assert response_data["error"] == "Username, email, and password are required fields."

def test_get_user(client):
    # Arrange
    user = User(username="testuser", email="test@example.com", password="testpassword")
    db.session.add(user)
    db.session.commit()

    # Act
    response = client.get(f"/users/{user.id}")

    # Assert
    assert response.status_code == 200
    response_data = response.get_json()
    assert "user" in response_data
    assert response_data["user"]["username"] == user.username
    assert response_data["user"]["email"] == user.email
