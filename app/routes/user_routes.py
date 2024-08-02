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

# @bp.put("/profile")
# @jwt_required()
# def update_profile():
#     data = request.get_json()
#     current_user_id = get_jwt_identity()

#     user = db.session.get(User, current_user_id)

#     if not user:
#         abort(make_response(dict(details="User not found"), 404))

#     try:
#         if 'username' in data:
#             user.username = data['username']
#         # Disallow email changes by not including it here
#         # Add other fields to update as necessary
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         abort(make_response(dict(details=f"Update failed: {str(e)}"), 400))

#     return dict(user=user.to_dict()), 200

# @bp.put("/profile/change-password")
# @jwt_required()
# def change_password():
#     data = request.get_json()
#     current_password = data.get('current_password')
#     new_password = data.get('new_password')
#     current_user_id = get_jwt_identity()

#     user = db.session.get(User, current_user_id)

#     if not current_password or not new_password:
#         abort(make_response(dict(details="Current password and new password are required"), 400))

#     if not user:
#         abort(make_response(dict(details="User not found"), 404))

#     if not check_password_hash(user.password, current_password):
#         abort(make_response(dict(details="Current password is incorrect"), 400))

#     try:
#         user.password = generate_password_hash(new_password)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         abort(make_response(dict(details=f"Password change failed: {str(e)}"), 400))

#     return dict(details="Password updated successfully"), 200