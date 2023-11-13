# EXTERNAL
from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS

# INTERNAL
from .profile.routes import profile
from .profile.models import db

app = Flask(__name__)

# Blueprints for each user story
app.register_blueprint(profile)

app.config.from_object(Config)

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

