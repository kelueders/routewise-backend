from ..config import test_client
from ..mock_data import MockData
from datetime import datetime

class TestItineraryRoute():
    
    # generate itinerary route
    def test_generate_itinerary(self, test_client):
        """Test generating an itinerary."""
        # populate database with trip and places
        trip_request = MockData.trip3_and_places_data
        test_client.post('/trip/add', json=trip_request)
        
        # test route
        response = test_client.patch('/itinerary/generate/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 1
        assert data['lastPlaceId'] == 5
        assert len(data['places']) == len(trip_request['trip']['places'])
        assert len(data['days']) == 3
        assert data['days']['day-1']['dateYYYYMMDD'] == trip_request['trip']['startDate']
        date_obj = datetime.strptime(trip_request['trip']['startDate'], '%Y/%m/%d').date()
        assert data['days']['day-1']['dateMMDD'] == date_obj.strftime('%m/%d')
        assert data['days']['day-1']['dateWeekdayMonthDay'] == date_obj.strftime('%A, %B %#d')
        assert data['days']['day-1']['weekday'] ==  date_obj.strftime('%a')
        assert data['days']['day-1']['dayNum'] == 'day-1'
        assert data['days']['day-1']['id'] == 1
        assert len(data['days']['day-1']['placeIds']) != 0
        assert len(data['dayOrder']) == 3
        assert data['dayOrder'][0] == 'day-1'
    
    def test_generate_itinerary_nonexisting_trip(self, test_client):
        """Test generating itinerary with nonexisting trip."""
        response = test_client.patch('/itinerary/generate/3')
        assert response.status_code == 404

    # add one place to itinerary route
    def test_add_one_place(self, test_client):
        """Test adding a place to trip where the itinerary is already created."""
        request = {
            'dayId': 2,
            'place': MockData.place1_data
        }
        request['place']['positionId'] = 6
        response = test_client.post('/itinerary/add-one-place/1', json=request)
        assert response.status_code == 200
        assert int(response.data.decode('utf-8')) == 6

    def test_add_one_place_no_day(self, test_client):
        """Test adding a place to a trip with no day attached."""
        request = {
            'dayId': None,
            'place': MockData.place1_data
        }
        request['place']['positionId'] = 7
        response = test_client.post('/itinerary/add-one-place/1', json=request)
        assert response.status_code == 200
        assert int(response.data.decode('utf-8')) == 7
