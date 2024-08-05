from flask import json

from app import db
from app.models.user import User


def test_create_user(client):
    # Arrange
    data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpassword"
    }

    # Act
    response = client.post("/users", data=json.dumps(data), content_type='application/json')

    # Assert
    assert response.status_code == 201
    response_data = response.get_json()
    assert "user" in response_data
    assert response_data["user"]["username"] == data["username"]
    assert response_data["user"]["email"] == data["email"]

def test_create_user_invalid_data(client):
    # Arrange
    data = {
        "username": "testuser"
        # missing email or other required fields
    }

    # Act
    response = client.post("/users", data=json.dumps(data), content_type='application/json')

    # Assert
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data["details"] == "Invalid data"

def test_get_user(client):
    # Arrange
    user = User(username="testuser", email="test@example.com", password="testpassword")
    db.session.add(user)
    db.session.commit()

    # Act
    response = client.get("/users")

    # Assert
    assert response.status_code == 200
    response_data = response.get_json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["username"] == user.username
    assert response_data[0]["email"] == user.email
