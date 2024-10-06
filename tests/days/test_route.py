from ..config import test_client
from ..mock_data import MockData
from datetime import datetime

class TestDaysRoute():
    
    # add trip and places
    def add_trip_with_places(self, test_client):
        # add user
        test_client.post('/profile/user', json=MockData.user1_data)

        # add trip and places
        request = MockData.trip2_and_places_data
        test_client.post('/trip/add', json=request)
    
    # update day name route
    def test_update_day_name(self, test_client):
        """Test updating day name."""
        self.add_trip_with_places(test_client)
        
        request = {
            'dayName': 'New fun name'
        }
        response = test_client.patch('/days/update-name/1', json=request)
        assert response.status_code == 200
