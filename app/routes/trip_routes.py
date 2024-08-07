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

    prompt = f"""
        Generate a detailed trip plan for visiting {trip_details['destination']} from {trip_details['start_date']} to {trip_details['end_date']} with a budget of {trip_details['budget']}. The plan should include the destination, latitude and longitude of the destination, start and end dates (from start day to end day included), budget (not more than the given budget), place to stay, an itinerary with days. Separate the itinerary into activities (what to do), places to eat. For each activity, place to eat, and place to stay include to approximate cost in the description.
        Format the response as follows:

        {{
        "destination": "{{trip_details['destination']}}",
        "latitude": "latitude_placeholder_as_float",
        "longitude": "longitude_placeholder_as_float",
        "start_date": "{{trip_details['start_date']}}",
        "end_date": "{{trip_details['end_date']}}",
        "budget": {{trip_details['budget']}},
        "PlaceToRest":{{
            "place": "place_name_placeholder",
            "latitude": "latitude_placeholder_as_float",
            "longitude": "longitude_placeholder_as_float",
            "description": "description_placeholder"
        }},
        "itinerary": [
            {{
            "day": 1,
            "activities": [
                {{
                "activity": "activity_name_placeholder",
                "latitude": "latitude_placeholder_as_float",
                "longitude": "longitude_placeholder_as_float",
                "description": "description_placeholder"
                }},
                ...
            ],
            "placesToEat": [
                {{
                "place": "place_name_placeholder",
                "latitude": "latitude_placeholder_as_float",
                "longitude": "longitude_placeholder_as_float",
                "description": "description_placeholder"
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
        start_date=itinerary_json['start_date'],
        end_date=itinerary_json['end_date'],
        budget=itinerary_json['budget'],
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

    return jsonify(trip.to_dict(), 201)

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