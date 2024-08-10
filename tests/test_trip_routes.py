from flask import json
from app import db
from app.models.trip import Trip


def save_trip(client):
    data = {
        "destination": "Los Angeles, CA",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "start_date": "2024-09-02",
        "end_date": "2024-09-02",
        "budget": 300,
        "description": "Explore the vibrant city of Los Angeles on a budget in one day.",
        "PlaceToRest": {
            "place": "Budget Inn",
            "latitude": 34.0489,
            "longitude": -118.2608,
            "description": "A budget-friendly accommodation option with basic amenities. Cost: $50 for the night."
        },
        "itinerary": [
            {
                "day": 1,
                "activities": [
                    {
                        "activity": "Visit Hollywood Walk of Fame",
                        "latitude": 34.1017,
                        "longitude": -118.3264,
                        "description": "Stroll along the famous sidewalk featuring stars of renowned celebrities. Free activity."
                    },
                    {
                        "activity": "Explore Griffith Observatory",
                        "latitude": 34.1184,
                        "longitude": -118.3004,
                        "description": "Enjoy panoramic views of LA and explore exhibits on space and science. Admission: $8 per person."
                    },
                    {
                        "activity": "Relax at Venice Beach",
                        "latitude": 33.9850,
                        "longitude": -118.4695,
                        "description": "Spend time by the beach, stroll the boardwalk, and people-watch. Free activity."
                    }
                ],
                "placesToEat": [
                    {
                        "place": "In-N-Out Burger",
                        "latitude": 34.0976,
                        "longitude": -118.3414,
                        "description": "Grab a delicious and affordable meal at this popular burger chain. Cost: $10 per person."
                    },
                    {
                        "place": "Grand Central Market",
                        "latitude": 34.0507,
                        "longitude": -118.2482,
                        "description": "Experience diverse food options at this historic indoor market. Cost: $15 per person."
                    }
                ]
            }
        ]
    }

    return client.post("/trips/save/5", data=json.dumps(data), content_type='application/json')

def test_save_trip(client):
    response = save_trip(client)
    
    # Assert
    assert response.status_code == 201
    response_data = response.get_json()
    
    # Asserting the details of the trip
    assert response_data['budget'] == 300
    assert response_data['destination'] == "Los Angeles, CA"
    assert response_data['itineraries'][0]['days'][0]['itinerary_id'] == response_data['itineraries'][0]['id']
    assert response_data['latitude'] == 34.0522
    assert response_data['longitude'] == -118.2437
    assert 'id' in response_data
    assert 'place_to_rest' in response_data
    assert response_data['start_date'] == "Mon, 02 Sep 2024 00:00:00 GMT"
    assert response_data['end_date'] == "Mon, 02 Sep 2024 00:00:00 GMT"
    assert response_data['user_id'] == 5

    # Asserting the details of the first day's activities in the first itinerary
    assert response_data['itineraries'][0]['days'][0]['activities'][0]['activity'] == "Visit Hollywood Walk of Fame"
    assert response_data['itineraries'][0]['days'][0]['activities'][0]['latitude'] == 34.1017
    assert response_data['itineraries'][0]['days'][0]['activities'][0]['longitude'] == -118.3264
    assert response_data['itineraries'][0]['days'][0]['activities'][1]['activity'] == "Explore Griffith Observatory"
    assert response_data['itineraries'][0]['days'][0]['activities'][1]['latitude'] == 34.1184
    assert response_data['itineraries'][0]['days'][0]['activities'][1]['longitude'] == -118.3004
    assert response_data['itineraries'][0]['days'][0]['activities'][2]['activity'] == "Relax at Venice Beach"
    assert response_data['itineraries'][0]['days'][0]['activities'][2]['latitude'] == 33.9850
    assert response_data['itineraries'][0]['days'][0]['activities'][2]['longitude'] == -118.4695

    # Asserting the places to eat on the first day in the first itinerary
    assert response_data['itineraries'][0]['days'][0]['places_to_eat'][0]['place'] == "In-N-Out Burger"
    assert response_data['itineraries'][0]['days'][0]['places_to_eat'][0]['latitude'] == 34.0976
    assert response_data['itineraries'][0]['days'][0]['places_to_eat'][0]['longitude'] == -118.3414
    assert response_data['itineraries'][0]['days'][0]['places_to_eat'][1]['place'] == "Grand Central Market"
    assert response_data['itineraries'][0]['days'][0]['places_to_eat'][1]['latitude'] == 34.0507
    assert response_data['itineraries'][0]['days'][0]['places_to_eat'][1]['longitude'] == -118.2482

    # Asserting the details of the place to rest
    assert response_data['place_to_rest']['place'] == "Budget Inn"
    assert response_data['place_to_rest']['latitude'] == 34.0489
    assert response_data['place_to_rest']['longitude'] == -118.2608

def test_save_trip_with_missing_place_to_rest(client):
    data = {
        "destination": "Chisinau, Moldova",
        "latitude": 47.0105,
        "longitude": 28.8638,
        "start_date": "2024-10-20",
        "end_date": "2024-10-29",
        "budget": 500,
        "description": "Explore the capital city of Moldova on a budget.",
        # Missing PlaceToRest entirely
        "itinerary": []
    }
    response = client.post("/trips/save/210", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400

def test_save_trip_with_missing_itinerary(client):
    data = {
        "destination": "Rome, Italy",
        "latitude": 41.9028,
        "longitude": 12.4964,
        "start_date": "2024-09-05",
        "end_date": "2024-10-01",
        "budget": 1350,
        "description": "Explore the historic city of Rome and enjoy authentic Italian cuisine.",
        "PlaceToRest": {
            "place": "Hotel Colosseum",
            "latitude": 41.8897,
            "longitude": 12.4903,
            "description": "Located close to the Colosseum, offering comfortable rooms and breakfast included. Approximate cost: $100 per night."
        },
        # Missing itinerary entirely
    }
    response = client.post("/trips/save/45", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    

def test_get_trip_by_id(client):
    save_trip_response = save_trip(client)
    assert save_trip_response.status_code == 201

    trip_id = save_trip_response.get_json()['id']

    # Act
    response = client.get(f"/trips/{trip_id}")
    response_data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert 'trip' in response_data
    trip_data = response_data['trip']

    # Asserting the basic details of the trip
    assert trip_data['budget'] == 300
    assert trip_data['destination'] == "Los Angeles, CA"
    assert trip_data['end_date'] == "Mon, 02 Sep 2024 00:00:00 GMT"
    assert trip_data['id'] == trip_id
    assert trip_data['latitude'] == 34.0522
    assert trip_data['longitude'] == -118.2437
    assert trip_data['start_date'] == "Mon, 02 Sep 2024 00:00:00 GMT"
    assert trip_data['user_id'] == 5
    assert 'description' in trip_data

    # Asserting the structure of the itineraries
    assert 'itineraries' in trip_data 
    assert len(trip_data['itineraries']) > 0

    # Asserting the structure of the first itinerary
    itinerary = trip_data['itineraries'][0]
    assert 'days' in itinerary

    # Asserting the structure of the first day
    day = itinerary['days'][0]
    assert 'activities' in day
    assert len(day['activities']) > 0 

    # Asserting the structure of the first activity
    activity = day['activities'][0]
    assert 'activity' in activity
    assert 'description' in activity
    assert 'latitude' in activity
    assert 'longitude' in activity

    # Asserting the structure of the places to eat
    assert 'places_to_eat' in day
    place_to_eat = day['places_to_eat'][0]
    assert 'description' in place_to_eat
    assert 'latitude' in place_to_eat
    assert 'longitude' in place_to_eat
    assert 'place' in place_to_eat

def test_save_trip_missing_required_fields(client):
    data = {
        # Omitting required fields
    }
    response = client.post("/trips/save/12", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400

def test_save_trip_invalid_date_range(client):
    data = {
        "destination": "Los Angeles, CA",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "start_date": "2024-09-03",  # Start date is after the end date
        "end_date": "2024-09-02",
        "budget": 300,
        # Other required fields...
    }
    response = client.post("/trips/save/5", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400

def test_save_trip_negative_budget(client):
    data = {
        "destination": "Seattle, WA",
        "latitude": 47.6062,
        "longitude": -122.3321,
        "budget": -100,  # Negative budget
        # Other required fields...
    }
    response = client.post("/trips/save/9", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400

def delete_trip(client):
    # Act
    response = client.delete("/trips/delete/1")

    # Assert
    assert response.status_code == 204

    trip = Trip.query.get(1)
    assert trip is None

def test_delete_trip_not_found(client):
    # Act
    response = client.delete("/trips/90")
    response_data = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_data == {
        "details": "Unknown Trip id: 90"
    }