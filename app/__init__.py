from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)                # the database is represented in the app by the database instance
migrate = Migrate(app, db)          # the instance for the database migration engine

from app import routes, models

