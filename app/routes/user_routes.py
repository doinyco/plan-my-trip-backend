from flask import Blueprint, abort, make_response, request, Response
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
    return ["hello world, testing"]