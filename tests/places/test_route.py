from ..config import test_client

class TestPlacesRoute():
    trip1_data = {
        "uid": "12345",
        "trip": {
            "name": "Paris",
            "city": "Paris",
            "state": "",
            "country": "France",
            "countryAbbr": "FR",
            "destLat": 48.8588897,
            "destLong": 2.3200410217200766,
            "destImgUrl": "https://images.unsplash.com/photo-1525218291292-e46d2a90f77c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1MzAyODV8MHwxfHNlYXJjaHwxfHxQYXJpcy1JbGUtZGUtRnJhbmNlLWxhbmRtYXJrc3xlbnwwfHx8fDE3MjYyNjYzMzR8MA&ixlib=rb-4.0.3&q=80&w=1080",
            "startDate": '2024-09-01',
            "endDate": '2024-09-05'
        }
    }

    trip2_and_places_data = {
        "uid": "12345",
        "trip": {
            "name": "new trip",
            "city": "Tokyo",
            "state": "",
            "country": "Japan",
            "countryAbbr": "JP",
            "geocode": [35.6828387, 139.7594549],
            "imgUrl": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1MzAyODV8MHwxfHNlYXJjaHwxfHxUb2t5by0tbGFuZG1hcmtzfGVufDB8fHx8MTcyNjMzMDE3OHww&ixlib=rb-4.0.3&q=80&w=1080",
            "startDate": "2024-09-15",
            "endDate": "2024-09-19",
            "places": [
                {
                    "positionId": 1,
                    "name": "Ghibli Museum",
                    "apiId": "ChIJLYwD5TTuGGARBZKEP5BV4U0",
                    "address": "1-chōme-1-83 Shimorenjaku, Mitaka, Tokyo 181-0013, Japan",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJLYwD5TTuGGARBZKEP5BV4U0/photos/AXCi2Q6LD18Ol_BDV0GatAqbc289S_95wWKTd-HyAUbhIgNylADNq0bdmF21KseRcRXSX96Kc-FjOmCz5us_I2U_VnOGO2kN_1MluBAzDI2C5ITvbt3r7sw3Rplg4hfmwKVgkI5zAbdNNkxYaPQSc75WyIk07maPuhH7_BjI/media?maxWidthPx=4800&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Establishment",
                    "favorite": False,
                    "phoneNumber": "",
                    "rating": "4.5",
                    "summary": "Whimsical museum dedicated to the famed animation studio with a play area, theater & rooftop garden.",
                    "website": "https://www.ghibli-museum.jp/",
                    "info": "Mon: 10:00 AM – 6:00 PM, Tue: Closed, Wed: 10:00 AM – 6:00 PM, Thu: 10:00 AM – 6:00 PM, Fri: 10:00 AM – 6:00 PM, Sat: 10:00 AM – 6:00 PM, Sun: 10:00 AM – 6:00 PM",
                    "lat": 35.696238,
                    "long": 139.5704317
                },
                {
                    "positionId": 2,
                    "name": "Family Mart",
                    "apiId": "ChIJz52D5KKJGGARADyKkye7pxA",
                    "address": "Japan, 〒135-0061 Tokyo, Koto City, Toyosu, 5-chōme−2−１０ 沢真ビル",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJz52D5KKJGGARADyKkye7pxA/photos/AXCi2Q4_wrKn1Z10eAUqdoyPuHRlH986jRVwSoQEneAzZX1axJtUpH3PhkGJ9CYDuafSsAF1VwITTx69S6w5j4PXvoSgBUqFh5lb-fsdAtlTxUc2kevrSobjRj8A1t1Sch9vZns7TolsjFJJ_s7ffZcZgAPge7LNjDqISu2j/media?maxWidthPx=2227&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Food",
                    "favorite": False,
                    "phoneNumber": "+81 3-5547-9032",
                    "rating": "2.2",
                    "summary": "",
                    "website": "https://as.chizumaru.com/famima/detailmap?account=famima&bid=27511",
                    "info": "Mon: Open 24 hours, Tue: Open 24 hours, Wed: Open 24 hours, Thu: Open 24 hours, Fri: Open 24 hours, Sat: Open 24 hours, Sun: Open 24 hours",
                    "lat": 35.6534761,
                    "long": 139.7955297
                }
            ]
        }
    }

    place1_data = {
        "positionId": 3,
        "name": "cherry blossom",
        "apiId": "ChIJ39GHSE71GGARnwBli1-HcHM",
        "address": "Japan, 〒211-0063 Kanagawa, Kawasaki, Nakahara Ward, Kosugimachi, 1-chōme−５２６−１７, Akiba Bld., 1階",
        "imgUrl": "https://places.googleapis.com/v1/places/ChIJ39GHSE71GGARnwBli1-HcHM/photos/AXCi2Q4K8EV0ZBGj1TbQVZBg0N744CgDOFGHjdQnqyLFyO3S6obRhNgl_4HpixJtkey0THktUxI34OaGAWrQFWwxemqLoYSpdWJR8Phu4fC0YJpxrM3xN9Xmt7W9UoPgprwy-oTJ29z-RrdQkaFlGVpgO_o1JFPGJVocyTHl/media?maxWidthPx=1387&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
        "category": "Restaurant",
        "favorite": False,
        "phoneNumber": "+81 50-5462-3014",
        "rating": "4.4",
        "summary": "",
        "website": "https://cherryblossom.foodre.jp/",
        "info": "Mon: 5:00 – 10:00 PM, Tue: 11:30 AM – 2:00 PM; 5:00 PM – 12:00 AM, Wed: 11:30 AM – 2:00 PM; 5:00 PM – 12:00 AM, Thu: 11:30 AM – 2:00 PM; 5:00 PM – 12:00 AM, Fri: 5:00 PM – 12:00 AM, Sat: 5:00 PM – 12:00 AM, Sun: 5:00 – 10:00 PM",
        "lat": 35.5783884,
        "long": 139.65884269999998
    }
    
    def test_add_trip(self, test_client):
        ## Test adding a new user to the database.
        user_data = {
            'uid': '12345',
            'username': 'testuser',
            'email': 'testuser@example.com'
        }

        test_client.post('/profile/user', json=user_data)

        response = test_client.post('/places/trip', json=self.trip1_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 1
        assert data['startDate'] == self.trip1_data["trip"]["startDate"]
        assert data['endDate'] == self.trip1_data['trip']['endDate']
        assert data['duration'] == 5
    
    def test_get_trips(self, test_client):
        """Test getting all trips from user."""
        response = test_client.get('/places/trips/12345')
        assert response.status_code == 200
        data = response.get_json()
        assert data[0]['id'] == 1
        assert data[0]['name'] == self.trip1_data['trip']['name']
        assert data[0]['userUid'] == self.trip1_data['uid']
        assert data[0]['destCity'] == self.trip1_data['trip']['city']
        assert data[0]['destCountry'] == self.trip1_data['trip']['country']
        assert data[0]['destCountryAbbr'] == self.trip1_data['trip']['countryAbbr']
        assert data[0]['destImgUrl'] == self.trip1_data['trip']['destImgUrl']
        assert data[0]['destLat'] == self.trip1_data['trip']['destLat']
        assert data[0]['destLong'] == self.trip1_data['trip']['destLong']
        assert data[0]['destState'] == self.trip1_data['trip']['state']
        assert data[0]['endDate'] == self.trip1_data['trip']['endDate']
        assert data[0]['startDate'] == self.trip1_data['trip']['startDate']
        assert data[0]['duration'] == 5
        assert data[0]['isItinerary'] == False
    
    def test_update_trip_name(self, test_client):
        """Test getting all trips from user."""
        new_trip = {
            'tripName': 'new trip name',
            'startDate': '',
            'endDate': ''
        }
        response = test_client.post('/places/update-trip/1', json=new_trip)
        assert response.status_code == 200
    
    def test_update_trip_date(self, test_client):
        """Test getting all trips from user."""
        new_trip = {
            'tripName': '',
            'startDate': '2024-09-01',
            'endDate': '2024-09-06'
        }
        response = test_client.post('/places/update-trip/1', json=new_trip)
        assert response.status_code == 200

    # delete trip
    def test_delete_trip(self, test_client):
        """Test deleting trip."""
        response = test_client.delete('/places/delete-trip/1')
        assert response.status_code == 200

    # add trip and places
    def test_add_trip_and_places(self, test_client):
        """Test adding a trip with a few places."""
        response = test_client.post('/places/add-trip-and-places', json=self.trip2_and_places_data)
        assert response.status_code == 200

    # add place
    def test_add_place(self, test_client):
        """Test getting all trips from user."""
        response = test_client.post('/places/add-place/1', json=self.place1_data)
        assert response.status_code == 200
        assert response.data.decode('utf-8') == self.place1_data['apiId']

    # get places
    def test_get_places(self, test_client):
        """Test getting all trips from user."""
        response = test_client.get('/places/get-places/1')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        place = data['3']
        assert place['address'] == self.place1_data['address']
        assert place['apiId'] == self.place1_data['apiId']
        assert place['avgVisitTime'] == 60
        assert place['category'] == self.place1_data['category']
        assert place['dayId'] == None
        assert place['favorite'] == False
        assert place['id'] == 3
        assert place['imgUrl'] == self.place1_data['imgUrl']
        assert place['inItinerary'] == False
        assert place['info'] == self.place1_data['info']
        assert place['lat'] == self.place1_data['lat']
        assert place['long'] == self.place1_data['long']
        assert place['name'] == self.place1_data['name']
        assert place['phoneNumber'] == self.place1_data['phoneNumber']
        assert place['positionId'] == 3
        assert place['rating'] == self.place1_data['rating']
        assert place['summary'] == self.place1_data['summary']
        assert place['tripId'] == 1
        assert place['website'] == self.place1_data['website']

    def test_get_places_no_trip(self, test_client):
        """Test getting all trips from user."""
        response = test_client.get('/places/get-places/3')
        assert response.status_code == 400
    
    # get trip
    def test_get_trip(self, test_client):
        """Test getting a trip that doesn't exist."""
        response = test_client.get('/places/trip/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['tripId'] == 1
        assert data['lastPlaceId'] == 3
        assert len(data['places']) == 3
        # assert len(data['days']) == 5
        # assert data['days']['day-1']['dateFormatted'] == self.trip2_and_places_data['trip']['startDate']
        # assert len(data['dayOrder']) == 5
        # assert data['dayOrder'][0] == 'day-1'

    def test_get_trip_no_trip(self, test_client):
        """Test getting a trip that doesn't exist."""
        response = test_client.get('/places/trip/5')
        assert response.status_code == 400