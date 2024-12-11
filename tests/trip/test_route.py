from ..config import test_client
from ..mock_data import MockData
from datetime import datetime

class TestTripRoute():
    
    # add trip route
    def test_add_trip(self, test_client):
        """Test adding trip to user."""
        test_client.post('/profile/user', json=MockData.user1_data)

        request = MockData.trip1_data
        response = test_client.post('/trip/add', json=request)
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 1
        assert data['startDate'] == request["trip"]["startDate"]
        assert data['endDate'] == request['trip']['endDate']
        assert data['duration'] == 5
    
    def test_add_trip_with_places(self, test_client):
        """Test adding trip with places to user."""
        test_client.post('/profile/user', json=MockData.user1_data)

        request = MockData.trip2_and_places_data
        response = test_client.post('/trip/add', json=request)
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 2
        assert data['startDate'] == request["trip"]["startDate"]
        assert data['endDate'] == request['trip']['endDate']
        assert data['duration'] == 5
    
    # get trip route
    def test_get_trip(self, test_client):
        """Test getting a trip and its places."""
        valid_trip = MockData.trip2_and_places_data
        response = test_client.get('/trip/2')
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 2
        assert data['lastPlaceId'] == 2
        assert len(data['places']) == 2
        assert len(data['days']) == 5
        assert data['days']['day-1']['dateMMDDYYYY'] == valid_trip['trip']['startDate']
        date_obj = datetime.strptime(valid_trip['trip']['startDate'], '%m/%d/%Y').date()
        assert data['days']['day-1']['dateMMDD'] == date_obj.strftime('%m/%d')
        assert data['days']['day-1']['dateWeekdayMonthDay'] == date_obj.strftime('%A, %B %#d')
        assert data['days']['day-1']['weekday'] ==  date_obj.strftime('%a')
        assert data['days']['day-1']['id'] == 'day-1'
        assert data['days']['day-1']['dayId'] == 6
        assert len(data['days']['day-1']['placeIds']) != None
        assert len(data['dayOrder']) == 5
        assert data['dayOrder'][0] == 'day-1'

    def test_get_trip_invalid_trip(self, test_client):
        """Test getting a trip that doesn't exist."""
        response = test_client.get('/trip/5')
        assert response.status_code == 400

    # get trips route
    def test_get_trips(self, test_client):
        """Test getting all trips from user."""
        valid_trip = MockData.trip1_data
        response = test_client.get('/trip/trips/12345')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['id'] == 1
        assert data[0]['name'] == valid_trip['trip']['name']
        assert data[0]['uid'] == valid_trip['uid']
        assert data[0]['city'] == valid_trip['trip']['city']
        assert data[0]['country'] == valid_trip['trip']['country']
        assert data[0]['countryAbbr'] == valid_trip['trip']['countryAbbr']
        assert data[0]['imgUrl'] == valid_trip['trip']['imgUrl']
        assert data[0]['lat'] == valid_trip['trip']['lat']
        assert data[0]['long'] == valid_trip['trip']['long']
        assert data[0]['state'] == valid_trip['trip']['state']
        assert data[0]['endDate'] == valid_trip['trip']['endDate']
        assert data[0]['startDate'] == valid_trip['trip']['startDate']
        assert data[0]['duration'] == 5
        assert data[0]['isItinerary'] == False

    def test_get_trips_invalid_user(self, test_client):
        """Test getting all trips from invalid user."""
        response = test_client.get('/trip/trips/123')
        assert response.status_code == 400

    # delete trip route
    def test_delete_trip(self, test_client):
        """Test deleting trip."""
        response = test_client.delete('/trip/delete/1')
        assert response.status_code == 200

    # update trip route
    def test_update_trip_name(self, test_client):
        """Test updating trip name."""
        new_trip = {
            'tripName': 'new trip name',
            'startDate': '',
            'endDate': ''
        }
        response = test_client.post('/trip/update/2', json=new_trip)
        assert response.status_code == 200
    
    def test_update_trip_date(self, test_client):
        """Test updating trip date."""
        new_trip = {
            'tripName': '',
            'startDate': '09/01/2024',
            'endDate': '09/06/2024'
        }
        response = test_client.post('/trip/update/2', json=new_trip)
        assert response.status_code == 200
        response = test_client.get('/trip/2')
        # check days deleted and recreated properly
        data = response.get_json()
        assert len(data['days']) == 6
        assert data['days']['day-1']['dateMMDDYYYY'] == new_trip['startDate']
        assert response.status_code == 200

    def test_update_trip_invalid_trip(self, test_client):
        """Test updating invalid trip date."""
        new_trip = {
            'tripName': '',
            'startDate': '09/01/2024',
            'endDate': '09/06/2024'
        }
        response = test_client.post('/trip/update/5', json=new_trip)
        assert response.status_code == 400
