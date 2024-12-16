from ..config import test_client
from ..mock_data import MockData
from datetime import datetime

class TestPlacesRoute():
    
    # add trip route
    def add_trip(self, test_client):
        test_client.post('/profile/user', json=MockData.user1_data)

        request = MockData.trip1_data
        test_client.post('/trip/add', json=request)
    
    def create_itinerary(self, test_client):
        valid_place = MockData.place2_data
        valid_place['id'] = 2
        test_client.post('/places/add/1', json=valid_place)
        
        valid_place = MockData.place3_data
        valid_place['id'] = 3
        test_client.post('/places/add/1', json=valid_place)

        valid_place = MockData.place4_data
        valid_place['id'] = 4
        test_client.post('/places/add/1', json=valid_place)
        
        valid_place = MockData.place5_data
        valid_place['id'] = 5
        test_client.post('/places/add/1', json=valid_place)

        test_client.patch('/itinerary/generate/1')
    
    # add place route
    def test_add_place(self, test_client):
        """Test adding place to trip."""
        self.add_trip(test_client)

        request_place = MockData.place1_data
        request_place['id'] = 1
        response = test_client.post('/places/add/1', json=request_place)
        assert response.status_code == 200
        assert response.get_json()['databaseId'] == request_place['id']

    # get places route
    def test_get_places(self, test_client):
        """Test getting all places in trip."""
        self.create_itinerary(test_client)

        valid_place = MockData.place5_data

        response = test_client.get('/places/1')
        assert response.status_code == 200
        data = response.get_json()
        place = data['5']
        assert len(data) == 5
        assert place['address'] == valid_place['address']
        assert place['apiId'] == valid_place['apiId']
        assert place['avgVisitTime'] == 60
        assert place['category'] == valid_place['category']
        assert place['dayDatabaseId'] != None
        assert place['favorite'] == False
        assert place['databaseId'] == 5
        assert place['imgUrl'] == valid_place['imgUrl']
        assert place['inItinerary'] == True
        assert place['info'] == valid_place['info']
        assert place['lat'] == valid_place['lat']
        assert place['long'] == valid_place['long']
        assert place['name'] == valid_place['name']
        assert place['phoneNumber'] == valid_place['phoneNumber']
        assert place['id'] == 5
        assert place['rating'] == valid_place['rating']
        assert place['summary'] == valid_place['summary']
        assert place['tripId'] == 1
        assert place['website'] == valid_place['website']

    def test_get_places_invalid_trip(self, test_client):
        """Test getting all places from nonexisting trip."""
        response = test_client.get('/places/3')
        assert response.status_code == 400
        
    def test_get_place_empty_trip(self, test_client):
        """Test getting places from an empty trip."""
        self.add_trip(test_client)
        response = test_client.get('/places/2')
        assert response.status_code == 200
        assert len(response.get_json()) == 0
    
    # delete place route
    def test_delete_place(self, test_client):
        """Test deleting place."""
        response = test_client.delete('/places/delete/2')
        assert response.status_code == 200

    def test_delete_nonexisting_place(self, test_client):
        """Test deleting nonexisting place."""
        response = test_client.delete('/places/delete/10')
        assert response.status_code == 400

    # update place route
    def test_update_place(self, test_client):
        """Test updating place."""
        request = {
            "dayId": 2,
            "inItinerary": True
        }
        response = test_client.patch('/places/update/1', json=request)
        assert response.status_code == 200

    def test_update_nonexisting_place(self, test_client):
        """Test updating nonexisting place."""
        request = {
            "dayId": 2,
            "inItinerary": True
        }
        response = test_client.patch('/places/update/10', json=request)
        assert response.status_code == 400

    # move/swap places in a day route
    def test_swap_days(self, test_client):
        """Test swapping all places in a day with another day."""
        reponse = test_client.patch('/itinerary/generate/1')
        
        request = {
            "sourceDayId": 1,
            "destDayId" : 2,
            "swap": True
        }
        response = test_client.patch('/places/move-days/1', json=request)
        assert response.status_code == 200

    def test_move_days(self, test_client):
        """Test moving all places in a day to another day."""
        request = {
            "sourceDayId": 2,
            "destDayId" : 3,
            "swap": False
        }
        response = test_client.patch('/places/move-days/1', json=request)
        assert response.status_code == 200

    def test_move_days_nonexisting_day(self, test_client):
        """Test moving places in a day to a nonexisting day."""
        request = {
            "sourceDayId": 5,
            "destDayId" : 2,
            "swap": False
        }
        response = test_client.patch('/places/move-days/1', json=request)
        assert response.status_code == 502
 
    # delete places route
    def test_delete_places(self, test_client):
        """Test deleting multiple places."""
        request = {
            "placeIds": [3, 1]
        }
        response = test_client.delete('/places/delete', json=request)
        assert response.status_code == 200

    def test_delete_nonexisting_places(self, test_client):
        """Test deleting nonexisting place."""
        request = {
            "placeIds": [10, 12]
        }
        response = test_client.delete('/places/delete', json=request)
        assert response.status_code == 400

    # delete all places in a trip route
    def test_delete_all_places(self, test_client):
        """Test deleting all places in a trip."""
        response = test_client.delete('/places/delete-all/1')
        assert response.status_code == 200

    def test_delete_all_places_nonexisting_trip(self, test_client):
        """Test deleting all places from nonexisting trip."""
        response = test_client.delete('/places/delete-all/5')
        assert response.status_code == 404