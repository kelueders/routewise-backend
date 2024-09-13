import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    # Setup the Flask app with testing configuration
    flask_app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://test:test@localhost/test_db',  # Replace with your test DB URI
    })

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()  # Create tables for the test
        yield testing_client  # The testing happens here
        with flask_app.app_context():
            db.drop_all()  # Clean up the test DB after tests are done