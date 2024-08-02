from flask import Blueprint, abort, make_response, request, jsonify, Response
from ..db import db
from ..models.trip import Trip
from openai import OpenAI
from ..models.user import User
from ..models.itinerary import Itinerary
from ..models.day import Day
from ..models.activity import Activity
from ..models.place_to_eat import PlaceToEat

bp = Blueprint("trip", __name__, url_prefix="/trips")

def get_openai_client():
    return OpenAI()

@bp.post("/generate-trip-plan")
def generate_trip_plan():
    trip_details = request.get_json()
    # prompt = f"""
    #     Generate a detailed trip plan for visiting {trip.destination} from {trip.start_date} to {trip.end_date} with a budget of {trip.budget} and include the latitude and longitude of each site/activity as well as the lat/long of the destination.
    # """
    prompt = f"""
        Generate a detailed trip plan for visiting {trip_details['destination']} from {trip_details['start_date']} to {trip_details['end_date']} with a budget of {trip_details['budget']}. The plan should include the destination, latitude and longitude of the destination, start and end dates, budget (not more than the given budget), and an itinerary with days. Separate the itinerary into activities (what to do) and places to eat.
        Format the response as follows:

        {{
        "destination": "{{trip_details['destination']}}",
        "latitude_destination": "latitude_placeholder_as_float",
        "longitude_destination": "longitude_placeholder_as_float",
        "start_date": "{{trip_details['start_date']}}",
        "end_date": "{{trip_details['end_date']}}",
        "budget": {{trip_details['budget']}},
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
            ]
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
    print(user_id)

    # user = db.session.query(User).get(user_id)
    # print(user.username)

    # trip_id = request.args.get("trip_id")
    itinerary_json = request.get_json()

    trip = Trip(
        destination=itinerary_json['destination'],
        latitude=itinerary_json['latitude_destination'],
        longitude=itinerary_json['longitude_destination'],
        start_date=itinerary_json['start_date'],
        end_date=itinerary_json['end_date'],
        budget=itinerary_json['budget'],
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



# @bp.get("/get-trip")
# def get_trip():
#     destination = request.args.get("destination")
#     # latitude_destination = request.args.get("latitude_destination")
#     # longitude_destination = request.args.get("longitude_destination")
#     start_date = request.args.get("start_date")
#     end_date = request.args.get("end_date")
#     budget = request.args.get("budget")

#     trip = Trip(
#         destination=destination,
#         # latitude_destination=latitude_destination,
#         # longitude_destination=longitude_destination,
#         start_date=start_date,
#         end_date=end_date,
#         budget=budget
#     )

#     trip_plan = generate_trip_plan(trip)
#     return jsonify({"trip_plan": trip_plan})
    

@bp.post("")
def create_trip():
    request_body = request.get_json()

    try:
        new_trip = Trip.from_dict(request_body)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(new_trip)
    db.session.commit()

    return dict(trip=new_trip.to_dict()), 201


@bp.delete("/<trip_id>")
def delete_trip(trip):
    db.session.delete(trip)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.get("/<int:trip_id>")
def get_trip(trip_id):
    # Query the database for the trip with the given trip_id
    trip = db.session.get(Trip, trip_id)

    if not trip:
        # If the trip is not found, return a 404 error
        abort(make_response(dict(details="Trip not found"), 404))

    # If the trip is found, return its data
    return trip.to_dict(), 200