from flask import Flask
import os
from dotenv import load_dotenv

from app.routes import auth_routes
from .db import db, migrate
from app.models.user import User
from app.models.trip import Trip
from .routes import user_routes
from .routes import trip_routes

load_dotenv()

def create_app(config=None):
    print("Testing Deployment and deployments is successful if this prints")
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(trip_routes.bp)
    app.register_blueprint(auth_routes.bp)
    return app