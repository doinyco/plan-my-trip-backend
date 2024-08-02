from flask import Blueprint, abort, make_response, request, Response, jsonify
from ..db import db
from ..models.user import User


bp = Blueprint("user", __name__, url_prefix="/users")

@bp.post("")
def create_goal():
    data = request.get_json()

    try:
        user = User.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(user)
    db.session.commit()

    return dict(user=user.to_dict()), 201

@bp.get("")
def get_user():
    query = db.select(User)
    users = db.session.scalars(query)

    return [user.to_dict() for user in users]


@bp.get("/test") # test out local env setup and initial deployment with this route
def print_test():
    return ["hello world"]


@bp.get("/<int:user_id>/trips")
def get_user_trips(user_id):
    user = db.session.query(User).get(user_id)

    if user is None:
        abort(make_response(dict(details="User not found"), 404))

    trips_data = []
    for trip in user.trips:
        trip_dict = {
            "destination": trip.destination,
            "latitude_destination": trip.latitude,
            "longitude_destination": trip.longitude,
            "start_date": trip.start_date.strftime('%Y-%m-%d'),
            "end_date": trip.end_date.strftime('%Y-%m-%d'),
            "budget": trip.budget,
            "itinerary": []
        }
        for itinerary in trip.itineraries:
            for day in itinerary.days:
                day_dict = {
                    "day": day.day_number,
                    "activities": [],
                    "placesToEat": []
                }
                for activity in day.activities:
                    day_dict["activities"].append({
                        "activity": activity.activity,
                        "latitude": activity.latitude,
                        "longitude": activity.longitude,
                        "description": activity.description
                    })
                for place in day.places_to_eat:
                    day_dict["placesToEat"].append({
                        "place": place.place,
                        "latitude": place.latitude,
                        "longitude": place.longitude,
                        "description": place.description
                    })
                trip_dict["itinerary"].append(day_dict)
        trips_data.append(trip_dict)

    return jsonify(trips_data), 200
