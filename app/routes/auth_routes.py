from flask import Blueprint, jsonify,session, request

from app.models.user import User
from app.db import db

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.post("/register")
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required fields.'}), 400
    
    # Check existing username
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists. Please choose a different one.'}), 400
    
    # Check existing email
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'error': 'Email address already registered. Please use a different email.'}), 400
    
    # Check password rules
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400
    if not any(char.isupper() for char in password):
        return jsonify({'error': 'Password must contain at least one uppercase letter.'}), 400
    if not any(char.isdigit() for char in password):
        return jsonify({'error': 'Password must contain at least one digit.'}), 400
    
    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'success': 'Registration successful. You can now log in.'}), 200

@bp.post("/login")
def login():
    data = request.get_json()
    username_or_email = data.get('username/email')
    password = data.get('password')
    
    # Check if the input is an email
    if '@' in username_or_email:
        user = User.query.filter_by(email=username_or_email).first()
    else:
        user = User.query.filter_by(username=username_or_email).first()

    if user and user.check_password(password):
        # Login successful, return user information
        return jsonify({'success': 'Login successful.', 'user': user.to_dict()}), 200
    else:
        return jsonify({'error': 'Invalid username or password. Please try again.'}), 401

@bp.get('/logout')
def logout():
    session.clear()  # Clear all session data, effectively logging out the user
    return jsonify({'success': 'You have been logged out.'}), 200
