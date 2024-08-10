from flask import Blueprint, request, jsonify, Response
from ..db import db
from ..models.trip import Trip
from openai import OpenAI
from ..models.itinerary import Itinerary
from ..models.day import Day
from ..models.activity import Activity
from ..models.place_to_eat import PlaceToEat
from ..models.place_to_rest import PlaceToRest
from .helpers import validate_model
from functools import wraps
from datetime import datetime

bp = Blueprint("trip", __name__, url_prefix="/trips")

def require_trip(fn):
    @wraps(fn)
    def wrapper(*args, trip_id, **kwargs):
        trip = validate_model(Trip, trip_id)
        return fn(*args, trip=trip, **kwargs)
    return wrapper

def get_openai_client():
    return OpenAI()

@bp.post("/generate-trip-plan")
def generate_trip_plan():
    trip_details = request.get_json()

    start_date = datetime.strptime(trip_details['start_date'], "%Y-%m-%d")
    end_date = datetime.strptime(trip_details['end_date'], "%Y-%m-%d")
    days = (end_date - start_date).days + 1

    prompt = f"""
        Generate a detailed trip plan for visiting {trip_details['destination']} for {days} days with a strict budget of ${trip_details['budget']}. The start date is {trip_details['start_date']} and the end date is {trip_details['end_date']}. 

        Please ensure that the total cost of the trip does not exceed the given budget of ${trip_details['budget']}. The plan should include:

        - The destination
        - Latitude and longitude of the destination
        - Start and end dates (from start day to end day included)
        - Budget (ensure all costs add up to no more than the given budget)
        - A place to stay, including approximate cost
        - An itinerary with daily activities and places to eat, each with approximate costs

        {{
        "destination": "{{trip_details['destination']}}",
        "latitude": "latitude_placeholder_as_float",
        "longitude": "longitude_placeholder_as_float",
        "start_date": "{{trip_details['start_date']}}",
        "end_date": "{{trip_details['end_date']}}",
        "budget": {{trip_details['budget']}},
        "description": "description_placeholder",
        "PlaceToRest":{{
            "place": "place_name_placeholder",
            "latitude": "latitude_placeholder_as_float",
            "longitude": "longitude_placeholder_as_float",
            "description": "description_placeholder", include approximate cost in the description
        }},
        "itinerary": [
            {{
            "day": 1,
            "activities": [
                {{
                "activity": "activity_name_placeholder",
                "latitude": "latitude_placeholder_as_float",
                "longitude": "longitude_placeholder_as_float",
                "description": "description_placeholder", include approximate cost in the description
                }},
                ...
            ],
            "placesToEat": [
                {{
                "place": "place_name_placeholder",
                "latitude": "latitude_placeholder_as_float",
                "longitude": "longitude_placeholder_as_float",
                "description": "description_placeholder", include approximate cost in the description
                }},
                ...
            ],
            }},
            ...
        ]
        }}
    """

    client = get_openai_client()  # modified this to avoid the need of creating a new client every time in import
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return(completion.choices[0].message.content)

@bp.post("/save/<user_id>")
def save_trip(user_id):
    itinerary_json = request.get_json()

    # Check for required fields
    required_fields = ['destination', 'latitude', 'longitude', 'start_date', 'end_date', 'budget', 'PlaceToRest', 'itinerary']
    missing_fields = [field for field in required_fields if field not in itinerary_json]
    if missing_fields:
        return jsonify({"error": "Missing required fields: " + ", ".join(missing_fields)}), 400

    start_date = datetime.strptime(itinerary_json['start_date'], "%Y-%m-%d")
    end_date = datetime.strptime(itinerary_json['end_date'], "%Y-%m-%d")

    place_data = itinerary_json['PlaceToRest']

    place_to_rest = PlaceToRest(
        place=place_data['place'],
        latitude=place_data['latitude'],
        longitude=place_data['longitude'],
        description=place_data['description']
    )

    trip = Trip(
        destination=itinerary_json['destination'],
        latitude=itinerary_json['latitude'],
        longitude=itinerary_json['longitude'],
        start_date=start_date,
        end_date=end_date,
        budget=itinerary_json['budget'],
        description=itinerary_json['description'],
        place_to_rest=place_to_rest,
        user_id=user_id
    )

    db.session.add(trip)
    db.session.commit()

    itinerary = Itinerary(
        trip_id=trip.id,
        user_id=user_id
    )

    db.session.add(itinerary)
    db.session.commit()

    for e in itinerary_json['itinerary']:
        day = Day(
            day_number=e['day'],
            itinerary_id=itinerary.id
        )
        db.session.add(day)
        db.session.commit()

        for activity_json in e['activities']:
            activity = Activity(
                activity=activity_json['activity'],
                latitude=activity_json['latitude'],
                longitude=activity_json['longitude'],
                description=activity_json['description'],
                day_id=day.id
            )
            db.session.add(activity)

        for place_to_eat_json in e['placesToEat']:
            place_to_eat = PlaceToEat(
                place=place_to_eat_json['place'],
                latitude=place_to_eat_json['latitude'],
                longitude=place_to_eat_json['longitude'],
                description=place_to_eat_json['description'],
                day_id=day.id
            )
            db.session.add(place_to_eat)
        
        db.session.commit()

    return jsonify(trip.to_dict()), 201

@bp.get("/<trip_id>")
@require_trip
def get_trip(trip):
    return dict(trip=trip.to_dict())

@bp.delete("/<int:trip_id>")
@require_trip
def delete_trip(trip):
    db.session.delete(trip)
    db.session.commit()

    return Response(status=204, mimetype="application/json")