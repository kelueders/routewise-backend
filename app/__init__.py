# EXTERNAL
from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS

# INTERNAL
from .profile.routes import profile
from .places.routes import places
from .itinerary.routes import itinerary
from .auth.routes import auth
from .days.routes import days
from .trip.routes import trip
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Blueprints for each user story
    app.register_blueprint(profile)
    app.register_blueprint(places)
    app.register_blueprint(itinerary)
    app.register_blueprint(auth)
    app.register_blueprint(days)
    app.register_blueprint(trip)


    db.init_app(app)
    migrate = Migrate(app, db)        # the instance for the database migration engine
    CORS(app)                         # what is this for?????

    # Test route
    @app.route('/')
    def kate():
        response_body = {
            "name": "Kate",
            "about": "I'm a full stack developer"
        }

        return response_body

    return app
