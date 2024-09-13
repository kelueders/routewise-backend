import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import pytest

from app.models import User, UserInfo, user_schema, db

class ProfileRouteTest():
    
    @pytest.fixture(autouse=True)
    def setup(self, test_client):
        """Sets up the test client and ensures a clean slate for each test."""
        self.client = test_client

    def setup_method(self):
        """Runs before every test to ensure a clean database."""
        db.session.begin_nested()

    def teardown_method(self):
        """Runs after every test to roll back any changes made during the test."""
        db.session.rollback()

    def test_add_user(self):
        """Test adding a new user to the database."""
        user_data = {
            'uid': '12345',
            'username': 'testuser',
            'email': 'testuser@example.com'
        }

        response = self.client.post('/profile/user', json=user_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['uid'] == '12345'
        assert data['username'] == 'testuser'
        assert data['email'] == 'testuser@example.com'
        assert data['hasAccess'] == False