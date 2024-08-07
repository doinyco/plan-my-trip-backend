from flask import Blueprint, jsonify
from ..db import db
from ..models.user import User
from .helpers import validate_model
from functools import wraps

bp = Blueprint("user", __name__, url_prefix="/users")

def require_user(fn):
    @wraps(fn)
    def wrapper(*args, user_id, **kwargs):
        user = validate_model(User, user_id)
        return fn(*args, user=user, **kwargs)
    return wrapper

@bp.get("/<int:user_id>")
@require_user
def get_one_user(user):
    return dict(user=user.to_dict()), 200
    
@bp.get("/<int:user_id>/trips")
@require_user
def get_user_trips(user):
    trips_data = []

    for trip in user.trips:
        trip_dict = {
            "destination": trip.destination,
            "latitude_destination": trip.latitude,
            "longitude_destination": trip.longitude,
            "start_date": trip.start_date.strftime('%Y-%m-%d'),
            "end_date": trip.end_date.strftime('%Y-%m-%d'),
            "budget": trip.budget,
            "itinerary": [],
            "id": trip.id
        }
        for itinerary in trip.itineraries:
            for day in itinerary.days:
                day_dict = {
                    "day": day.day_number,
                    "activities": [],
                    "placesToEat": [],
                    "placesToRest": []
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
                for place in day.places_to_rest:
                    day_dict["placesToRest"].append({
                        "place": place.place,
                        "latitude": place.latitude,
                        "longitude": place.longitude,
                        "description": place.description
                    })
                trip_dict["itinerary"].append(day_dict)
        trips_data.append(trip_dict)

    return jsonify(trips_data), 200