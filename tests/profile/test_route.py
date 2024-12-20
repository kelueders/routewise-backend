from ..config import test_client
from ..mock_data import MockData

class TestProfileRoute():
    
    # add user route
    def test_add_user(self, test_client):
        """Test adding a new user to the database."""
        request = MockData.user1_data
        response = test_client.post('/profile/user', json=request)
        assert response.status_code == 200
        data = response.get_json()
        assert data['uid'] == request['uid']
        assert data['username'] == request['username']
        assert data['email'] == request['email']
        assert data['hasAccess'] == False
    
    def test_add_user_existing(self, test_client):
        """Test adding an existing user to the database."""
        response = test_client.post('/profile/user', json=MockData.user1_data)
        assert response.status_code == 400
    
    # add user info route
    def test_user_info(self, test_client):
        """Test adding user info to existing user."""
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

        response = test_client.post('/profile/user-info', json=user_info_data)
        assert response.status_code == 200
    
    def test_user_info_invalid_user(self, test_client):
        """Test adding user info to nonexisting user."""
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

        response = test_client.post('/profile/user-info', json=user_info_data)
        assert response.status_code == 400

    def test_get_user_info(self, test_client):
        """Test adding user info to nonexisting user."""
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

        response = test_client.get('/profile/user-info', json=user_info_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['uid'] == user_info_data['uid']
        assert data['shopping'] == user_info_data['categories']['shopping']
        assert data['nature'] == user_info_data['categories']['nature']
        assert data['landmarks'] == user_info_data['categories']['landmarks']
        assert data['entertainment'] == user_info_data['categories']['entertainment']
        assert data['relaxation'] == user_info_data['categories']['relaxation']
        assert data['food'] == user_info_data['categories']['food']
        assert data['arts'] == user_info_data['categories']['arts']

    def test_get_user_info_invalid_user(self, test_client):
        """Test adding user info to nonexisting user."""
        user_info_data = {
            "uid": "123345"
        }

        response = test_client.get('/profile/user-info', json=user_info_data)
        assert response.status_code == 400