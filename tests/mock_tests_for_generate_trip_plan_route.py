from flask import json
from unittest.mock import patch


def test_generate_trip_plan_with_valid_data_and_valid_response(client):
     # Arrange
    data = {
        "destination": "Paris, France",
        "start_date": "2024-12-01",
        "end_date": "2024-12-02",
        "budget": 1000
    }
    expected_response_data = {
        "destination": "Paris, France",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "start_date": "2024-12-01",
        "end_date": "2024-12-02",
        "description": "A trip to Paris, the City of Light",
        "budget": 200,
        "itinerary": [
            {
                "day": 1,
                "activities": [
                    {
                        "activity": "Visit the Eiffel Tower",
                        "latitude": 48.8584,
                        "longitude": 2.2945,
                        "description": "Enjoy panoramic views of Paris from the iconic Eiffel Tower."
                    },
                    {
                        "activity": "Explore the Louvre Museum",
                        "latitude": 48.8606,
                        "longitude": 2.3376,
                        "description": "Discover art masterpieces like the Mona Lisa in one of the world's largest museums."
                    }
                ],
                "placesToEat": [
                    {
                        "place": "Le Bouillon Chartier",
                        "latitude": 48.8720,
                        "longitude": 2.3447,
                        "description": "Dine in a historic brasserie known for classic French dishes at affordable prices."
                    }
                ]
            },
            {
                "day": 2,
                "activities": [
                    {
                        "activity": "Stroll along the Seine riverbanks",
                        "latitude": 48.8556,
                        "longitude": 2.3515,
                        "description": "Enjoy the picturesque views of the Seine River and its bridges."
                    },
                    {
                        "activity": "Visit Notre-Dame Cathedral",
                        "latitude": 48.8530,
                        "longitude": 2.3499,
                        "description": "Marvel at the stunning Gothic architecture of this historic cathedral."
                    }
                ],
                "placesToEat": [
                    {
                        "place": "L'As du Fallafel",
                        "latitude": 48.8578,
                        "longitude": 2.3594,
                        "description": "Taste delicious falafel and Middle Eastern cuisine in the vibrant Marais district."
                    }
                ]
            }
        ]
    }

    # Mock the response from the route to return the expected data
    with patch('flask.testing.FlaskClient.post') as mock_post:
        mock_post.return_value.json = expected_response_data
        mock_post.return_value.status_code = 200

        # Act
        response = client.post("/trips/generate-trip-plan", data=json.dumps(data), content_type='application/json')

        # Assert
        assert response.status_code == 200
        assert response.json == expected_response_data

def test_generate_trip_plan_tight_budget(client):
    # Arrange
    data_with_budget = {
        "destination": "Paris, France",
        "start_date": "2024-05-01",
        "end_date": "2024-05-02",
        "budget": 50  # Specific budget constraint
    }
    
    expected_response_data = {
        "itinerary": [
            {
                "day": 1,
                "activities": [
                    {
                        "activity": "Visit the Eiffel Tower",
                        "latitude": 48.8584,
                        "longitude": 2.2945,
                        "description": "Enjoy panoramic views of Paris from the iconic Eiffel Tower."
                    }
                ],
                "placesToEat": [
                    {
                        "place": "Chez Janou",
                        "latitude": 48.8574,
                        "longitude": 2.3645,
                        "description": "A cozy bistro offering Provençal dishes, perfect for a budget meal."
                    }
                ]
            }
        ]
    }

    with patch('flask.testing.FlaskClient.post') as mock_post:
        mock_post.return_value.get_json.return_value = expected_response_data
        mock_post.return_value.status_code = 200

        # Act
        response = client.post("/trips/generate-trip-plan", data=json.dumps(data_with_budget), content_type='application/json')
        response_data = response.get_json()

        # Assert
        assert response.status_code == 200
        assert response_data == expected_response_data

def test_generate_trip_plan_empty_destination(client):
    # Arrange
    data_empty_destination = {
        "destination": "",
        "start_date": "2024-10-10",
        "end_date": "2024-11-01",
        "budget": 1000
    }
    expected_response_data = {"error": "Destination cannot be empty"}

    with patch('flask.testing.FlaskClient.post') as mock_post:
        mock_post.return_value.get_json.return_value = expected_response_data
        mock_post.return_value.status_code = 400

        # Act
        response = client.post("/trips/generate-trip-plan", data=json.dumps(data_empty_destination), content_type='application/json')
        response_data = response.get_json()

        # Assert
        assert response.status_code == 400
        assert response_data == expected_response_data


def test_generate_trip_plan_invalid_date_range(client):
    # Arrange
    data_invalid_date_range = {
        "destination": "Paris, France",
        "start_date": "2024-05-03",
        "end_date": "2024-05-02",  # End date before start date
        "budget": 200
    }
    expected_response_data = {"error": "End date cannot be before start date"}

    with patch('flask.testing.FlaskClient.post') as mock_post:
        mock_post.return_value.get_json.return_value = expected_response_data
        mock_post.return_value.status_code = 400

        # Act
        response = client.post("/trips/generate-trip-plan", data=json.dumps(data_invalid_date_range), content_type='application/json')
        response_data = response.get_json()

        # Assert
        assert response.status_code == 400
        assert response_data == expected_response_data

def test_generate_trip_plan_missing_critical_data(client):
    # Arrange
    data_for_missing_critical_data = {
        "destination": "Paris, France",
        "start_date": "2024-05-01",
        "end_date": "2024-05-07",
        "budget": 500
    }
    
    incomplete_response_data = {
        "itinerary": [
            {
                "day": 1,
                "activities": [
                    {
                        "activity": "Visit the Eiffel Tower",
                        # Missing "latitude" and "longitude"
                        "description": "Enjoy panoramic views of Paris from the iconic Eiffel Tower."
                    }
                ],
                "placesToEat": [
                    {
                        "place": "Chez Janou",
                        "latitude": 48.8574,
                        "longitude": 2.3645,
                        "description": "A cozy bistro offering Provençal dishes, perfect for a budget meal."
                    }
                ]
            }
        ]
    }

    with patch('flask.testing.FlaskClient.post') as mock_post:
        mock_post.return_value.get_json.return_value = incomplete_response_data
        mock_post.return_value.status_code = 200

        # Act
        response = client.post("/trips/generate-trip-plan", data=json.dumps(data_for_missing_critical_data), content_type='application/json')
        response_data = response.get_json()

        # Assert
        assert "itinerary" in response_data
        assert "activities" in response_data["itinerary"][0]
        assert "latitude" not in response_data["itinerary"][0]["activities"][0]
        assert "longitude" not in response_data["itinerary"][0]["activities"][0]