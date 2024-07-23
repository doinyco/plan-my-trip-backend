from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.trip import Trip


bp = Blueprint("trip", __name__, url_prefix="/trips")

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