from ..config import test_client
from ..mock_data import MockData
from datetime import datetime

class TestPlacesRoute():
    
    # add trip route
    def test_add_trip(self, test_client):
        """Test adding trip to user."""
        test_client.post('/profile/user', json=MockData.user1_data)

        request = MockData.trip1_data
        response = test_client.post('/places/trip', json=request)
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 1
        assert data['startDate'] == request["trip"]["startDate"]
        assert data['endDate'] == request['trip']['endDate']
        assert data['duration'] == 5
    
    # get trips route
    def test_get_trips(self, test_client):
        """Test getting all trips from user."""
        valid_trip = MockData.trip1_data
        response = test_client.get('/places/trips/12345')
        assert response.status_code == 200
        data = response.get_json()
        print(data)
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
        response = test_client.get('/places/trips/123')
        assert response.status_code == 400

    # update trip route
    def test_update_trip_name(self, test_client):
        """Test updating trip name."""
        new_trip = {
            'tripName': 'new trip name',
            'startDate': '',
            'endDate': ''
        }
        response = test_client.post('/places/update-trip/1', json=new_trip)
        assert response.status_code == 200
    
    def test_update_trip_date(self, test_client):
        """Test updating trip date."""
        new_trip = {
            'tripName': '',
            'startDate': '2024/09/01',
            'endDate': '2024/09/06'
        }
        response = test_client.post('/places/update-trip/1', json=new_trip)
        assert response.status_code == 200

    def test_update_trip_invalid_trip(self, test_client):
        """Test updating invalid trip date."""
        new_trip = {
            'tripName': '',
            'startDate': '2024/09/01',
            'endDate': '2024/09/06'
        }
        response = test_client.post('/places/update-trip/5', json=new_trip)
        assert response.status_code == 400

    # delete trip route
    def test_delete_trip(self, test_client):
        """Test deleting trip."""
        response = test_client.delete('/places/delete-trip/1')
        assert response.status_code == 200

    # add trip and places route
    def test_add_trip_and_places(self, test_client):
        """Test adding a trip with a few places."""
        response = test_client.post('/places/add-trip-and-places', json=MockData.trip2_and_places_data)
        assert response.status_code == 200

    # add place route
    def test_add_place(self, test_client):
        """Test adding place to trip."""
        request_place = MockData.place1_data
        request_place['positionId'] = 3
        response = test_client.post('/places/add-place/1', json=request_place)
        assert response.status_code == 200
        assert response.data.decode('utf-8') == request_place['apiId']

    # get places route
    def test_get_places(self, test_client):
        """Test getting all places in trip."""
        valid_place = MockData.place1_data
        response = test_client.get('/places/get-places/1')
        assert response.status_code == 200
        data = response.get_json()
        place = data['3']
        assert len(data) == 3
        assert place['address'] == valid_place['address']
        assert place['apiId'] == valid_place['apiId']
        assert place['avgVisitTime'] == 60
        assert place['category'] == valid_place['category']
        assert place['dayId'] == None
        assert place['favorite'] == False
        assert place['id'] == 3
        assert place['imgUrl'] == valid_place['imgUrl']
        assert place['inItinerary'] == False
        assert place['info'] == valid_place['info']
        assert place['lat'] == valid_place['lat']
        assert place['long'] == valid_place['long']
        assert place['name'] == valid_place['name']
        assert place['phoneNumber'] == valid_place['phoneNumber']
        assert place['positionId'] == 3
        assert place['rating'] == valid_place['rating']
        assert place['summary'] == valid_place['summary']
        assert place['tripId'] == 1
        assert place['website'] == valid_place['website']

    def test_get_places_invalid_trip(self, test_client):
        """Test getting all places from nonexisting trip."""
        response = test_client.get('/places/get-places/3')
        assert response.status_code == 400
    
    # get trip route
    def test_get_trip(self, test_client):
        """Test getting a trip and its places."""
        valid_trip = MockData.trip2_and_places_data
        response = test_client.get('/places/trip/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 1
        assert data['lastPlaceId'] == 3
        assert len(data['places']) == 3
        assert len(data['days']) == 5
        assert data['days']['day-1']['dateYYYYMMDD'] == valid_trip['trip']['startDate']
        date_obj = datetime.strptime(valid_trip['trip']['startDate'], '%Y/%m/%d').date()
        assert data['days']['day-1']['dateMMDD'] == date_obj.strftime('%m/%d')
        assert data['days']['day-1']['dateWeekdayMonthDay'] == date_obj.strftime('%A, %B %#d')
        assert data['days']['day-1']['weekday'] ==  date_obj.strftime('%a')
        assert data['days']['day-1']['dayNum'] == 'day-1'
        assert data['days']['day-1']['id'] == 1
        assert len(data['days']['day-1']['placeIds']) != None
        assert len(data['dayOrder']) == 5
        assert data['dayOrder'][0] == 'day-1'

    def test_get_trip_invalid_trip(self, test_client):
        """Test getting a trip that doesn't exist."""
        response = test_client.get('/places/trip/5')
        assert response.status_code == 400