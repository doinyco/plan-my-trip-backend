from flask import Flask
# from flask_cors import CORS
import os
from dotenv import load_dotenv
from app.routes import auth_routes, user_routes, trip_routes
from .db import db, migrate

# Load environment variables from a .env file if it exists
load_dotenv()

def create_app(config=None):
    print("Testing Deployment and deployments is successful if this prints")
    
    app = Flask(__name__)
    
    # Set default configuration values
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'plan_my_trip')  # Ensure SECRET_KEY is set
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')

    if config:
        app.config.update(config)

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(trip_routes.bp)
    app.register_blueprint(auth_routes.bp)
    
    # Enable CORS
    # CORS(app)
    
    return app
