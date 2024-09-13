import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import pytest
from tests.config import test_client
from app.models import User, UserInfo, user_schema, db

class TestProfileRoute():
    
    def test_add_user(self, test_client):
        """Test adding a new user to the database."""
        user_data = {
            'uid': '12345',
            'username': 'testuser',
            'email': 'testuser@example.com'
        }

        response = test_client.post('/profile/user', json=user_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['uid'] == '12345'
        assert data['username'] == 'testuser'
        assert data['email'] == 'testuser@example.com'
        assert data['hasAccess'] == False
    
    def test_add_user_exisitng(self, test_client):
        """Test adding an existing user to the database."""
        user_data = {
            'uid': '12345',
            'username': 'testuser',
            'email': 'testuser@example.com'
        }

        response = test_client.post('/profile/user', json=user_data)
        assert response.status_code == 400
    
    def test_user_info(self, test_client):
        """Test adding a new user to the database."""
        user_info_data = {
            "uid": "12345",
            "categories": {
                "shopping": True,
                "nature": True,
                "landmarks": False,
                "entertainment": True,
                "relaxation": False,
                "food": False,
                "arts": False
            }
        }

        response = test_client.post('/profile/user_info', json=user_info_data)
        assert response.status_code == 200
    
    def test_user_info_fail(self, test_client):
        """Test adding a new user to the database."""
        user_info_data = {
            "uid": "123345",
            "categories": {
                "shopping": True,
                "nature": True,
                "landmarks": False,
                "entertainment": True,
                "relaxation": False,
                "food": False,
                "arts": False
            }
        }

        response = test_client.post('/profile/user_info', json=user_info_data)
        assert response.status_code == 400