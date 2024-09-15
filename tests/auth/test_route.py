from ..config import test_client
from ..mock_data import MockData

class TestAuthRoute():
    
    # check code route
    def test_check_code_invalid_user(self, test_client):
        """Test checking non-existing user access."""
        request = {
            'uid': '12345',
            'passcode': '14453'
        }

        response = test_client.get('/auth/check-code', json=request)
        assert response.status_code == 400
    
    def test_check_code_denied(self, test_client):
        """Test checking unauthorized user access."""
        test_client.post('/profile/user', json=MockData.user1_data)

        request = {
            'uid': '12345',
            'passcode': '14453'
        }
        response = test_client.get('/auth/check-code', json=request)
        assert response.status_code == 401

    def test_check_code_granted(self, test_client):
        """Test granting unauthorized user access."""
        test_client.post('/profile/user', json=MockData.user1_data)

        request = {
            'uid': '12345',
            'passcode': '124453'
        }
        response = test_client.patch('/auth/check-code', json=request)
        assert response.status_code == 200