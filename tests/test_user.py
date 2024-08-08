# tests/test_user.py
from datetime import datetime
import pytest
from app import create_app, db
from app.models.trip import Trip
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

def test_get_user_trips(client):
    # Arrange
    user = User(username="testuser", email="test@example.com", password="testpassword")
    db.session.add(user)
    db.session.commit()

    # Create trips associated with the user
    trip1 = Trip(
        destination="Paris",
        latitude=48.8566,
        longitude=2.3522,
        start_date=datetime.strptime("2024-08-10", "%Y-%m-%d").date(),
        end_date=datetime.strptime("2024-08-20", "%Y-%m-%d").date(),
        budget=2000,
        user_id=user.id
    )
    trip2 = Trip(
        destination="New York",
        latitude=40.7128,
        longitude=-74.0060,
        start_date=datetime.strptime("2024-09-01", "%Y-%m-%d").date(),
        end_date=datetime.strptime("2024-09-10", "%Y-%m-%d").date(),
        budget=3000,
        user_id=user.id
    )
    db.session.add_all([trip1, trip2])
    db.session.commit()

    # Act
    response = client.get(f"/users/{user.id}/trips")

    # Assert
    assert response.status_code == 200
    response_data = response.get_json()
    assert len(response_data) == 2

    trip_destinations = [trip["destination"] for trip in response_data]
    assert "Paris" in trip_destinations
    assert "New York" in trip_destinations

    # Check the structure of the first trip
    trip = response_data[0]
    assert "destination" in trip
    assert "latitude_destination" in trip
    assert "longitude_destination" in trip
    assert "start_date" in trip
    assert "end_date" in trip
    assert "budget" in trip
    assert "place_to_rest" in trip
    assert "itinerary" in trip

    # Check that the `place_to_rest` and `itinerary` are empty (as set up)
    assert trip["place_to_rest"] == {}
    assert trip["itinerary"] == []

def test_get_user_trips_no_trips(client):
    # Arrange
    user = User(username="testuser", email="test@example.com", password="testpassword")
    db.session.add(user)
    db.session.commit()

    # Act
    response = client.get(f"/users/{user.id}/trips")

    # Assert
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == []