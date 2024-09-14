from ..config import test_client

class TestAuthRoute():
    
    def test_check_code_no_user(self, test_client):
        """Test checking non-existing user access."""
        user_access_data = {
            'uid': '12345',
            'passcode': '14453'
        }

        response = test_client.get('/auth/check-code', json=user_access_data)
        assert response.status_code == 400
    
    def test_check_code_denied(self, test_client):
        """Test checking unauthorized user access."""
        user_data = {
            'uid': '12345',
            'username': 'testuser',
            'email': 'testuser@example.com'
        }

        test_client.post('/profile/user', json=user_data)

        user_access_data = {
            'uid': '12345',
            'passcode': '14453'
        }

        response = test_client.get('/auth/check-code', json=user_access_data)
        assert response.status_code == 401

    def test_check_code_granted(self, test_client):
        """Test checking unauthorized user access."""
        user_data = {
            'uid': '12345',
            'username': 'testuser',
            'email': 'testuser@example.com'
        }

        test_client.post('/profile/user', json=user_data)

        user_access_data = {
            'uid': '12345',
            'passcode': '124453'
        }

        response = test_client.patch('/auth/check-code', json=user_access_data)
        assert response.status_code == 200