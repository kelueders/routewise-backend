import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture(scope='module')
def test_client():
    # Setup the Flask app with testing configuration
    flask_app = create_app(TestConfig)
    testing_client = flask_app.test_client()
    with flask_app.app_context():
        db.create_all()  # Create tables for the test

        yield testing_client  # The testing happens here

        db.drop_all()  # Clean up the test DB after tests are done