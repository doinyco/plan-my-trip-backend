from flask import Blueprint, abort, make_response, request, jsonify
from ..db import db
from ..models.trip import Trip
from openai import OpenAI
from ..models.user import User

bp = Blueprint("trip", __name__, url_prefix="/trips")
client = OpenAI()


@bp.post("/generate-trip-plan")
def generate_trip_plan():
    trip_details = request.get_json()
    
    # Prompt for the OpenAI API
    prompt = f"""
        Generate a detailed trip plan in JSON format for visiting {{trip_details['destination']}} from {{trip_details['start_date']}} to {{trip_details['end_date']}} with a budget of {{trip_details['budget']}}. The plan should include the destination, latitude and longitude of the destination, start and end dates, budget (not more than the given budget), and an itinerary with days. Separate the itinerary into activities (what to do) and places to eat. Format the response as follows:

        {{
        "destination": "{{trip_details['destination']}}",
        "latitude_destination": "latitude_placeholder",
        "longitude_destination": "longitude_placeholder",
        "start_date": "{{trip_details['start_date']}}",
        "end_date": "{{trip_details['end_date']}}",
        "budget": {{trip_details['budget']}},
        "itinerary": [
            {{
            "day": 1,
            "activities": [
                {{
                "activity": "activity_name_placeholder",
                "latitude": "latitude_placeholder",
                "longitude": "longitude_placeholder",
                "description": "description_placeholder"
                }},
                ...
            ],
            "placesToEat": [
                {{
                "place": "place_name_placeholder",
                "latitude": "latitude_placeholder",
                "longitude": "longitude_placeholder",
                "description": "description_placeholder"
                }},
                ...
            ]
            }},
            ...
        ]
        }}
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return(completion.choices[0].message.content)

@bp.post("")
def post_trip():
    data = request.get_json()

    try:
        trip = Trip.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(trip)
    db.session.commit()

    return dict(trip=trip.to_dict()), 201

@bp.get("")
def get_user():
    query = db.select(Trip)
    trips = db.session.scalars(query)

    return [trip.to_dict() for trip in trips]