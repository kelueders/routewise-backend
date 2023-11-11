# EXTERNAL
from flask import Flask
from config import Config
from flask_migrate import Migrate


# INTERNAL
from .profile.routes import profile
from .profile.models import db

app = Flask(__name__)

app.register_blueprint(profile)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)        # the instance for the database migration engine

# Test route
@app.route('/kate')
def kate():
    response_body = {
        "name": "Kate",
        "about": "I'm a full stack developer"
    }

    return response_body

