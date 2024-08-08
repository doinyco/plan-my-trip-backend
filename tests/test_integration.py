import pytest
from app.models.user import User
from unittest.mock import patch, Mock

@pytest.fixture
def user(client):
    # Register a user
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Password1'
    })
    assert response.status_code == 200

    # Log in the user
    response = client.post('/auth/login', json={
        'username/email': 'testuser',
        'password': 'Password1'
    })
    assert response.status_code == 200
    user = User.query.filter_by(username='testuser').first()
    return user

@patch('app.routes.trip_routes.OpenAI')  # Mock the OpenAI API client
def test_complete_flow(mock_openai, client, user, auth_header):
    # Mock response from OpenAI API
    mock_openai.return_value.chat_completions_create.return_value.choices = [
        type('obj', (object,), {'message': type('obj', (object,), {'content': '{"destination": "Paris", "latitude": 48.8566, "longitude": 2.3522, "start_date": "2024-08-01", "end_date": "2024-08-10", "budget": 2000, "itinerary": []}'})})()
    ]
    
    # Step 1: User registers and logs in (already handled in user fixture)
    
    # Step 2: Generate a trip plan
    response = client.post('/trips/generate-trip-plan', json={
        'destination': 'Paris',
        'start_date': '2024-08-01',
        'end_date': '2024-08-10',
        'budget': 2000
    }, headers=auth_header)

    # Debugging statements
    print("Response status code:", response.status_code)
    print("Response data:", response.data)
    
    # Ensure response status code is 200
    assert response.status_code == 200

# Ensure that your mock setup in `conftest.py` aligns with the routes being tested
@pytest.fixture(scope='session', autouse=True)
def mock_openai():
    # Mock the OpenAI client early
    with patch('app.routes.trip_routes.OpenAI') as mock_openai:
        mock_instance = Mock()
        mock_instance.chat_completions_create.return_value.choices = [
            type('obj', (object,), {'message': type('obj', (object,), {'content': '{"destination": "Paris", "latitude": 48.8566, "longitude": 2.3522, "start_date": "2024-08-01", "end_date": "2024-08-10", "budget": 2000, "itinerary": []}'})})()
        ]
        mock_openai.return_value = mock_instance
        yield mock_openai
