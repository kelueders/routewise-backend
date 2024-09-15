from .models import Place, db, place_schema, day_schema

def create_day_dict(day_num, day):
    '''
    {
        'dateMMDD': '09/15', 
        'dateWeekdayMonthDay': 'Sunday, September 15', 
        'dateYYYYMMDD': '2024/09/15', 
        'id': 'day-1', 
        'name': '', 
        'placeIds': [2, 4, 5], 
        'weekday': 'Sun'
    }
    '''
    id = f'day-{day_num}'
    day_dict = day_schema.dump(day)
    day_dict['id'] = id
    day_dict['placeIds'] = []
    return day_dict

def serialize_places(places):
    '''
    Serializes a list of Places.
        Returns a dictionary with  that each have a local_id as the KEY and the 
        place data (a dict) as the VALUE for each place

    {
        1: {
            "local_id": 1,
            "placeName": "Hyde Park",
            "address": "Hyde Park, Albion Street, London, W2 2LG, United Kingdom",
            "imgUrl": "https://images.unsplash.com/",
            "place_id": 2535,
            "info": "No hours information",
            "lat": 51.5074889,
            "long": -0.162236683080672,
            "favorite": false,
            "category": "park",
            "phoneNumber": "604-000-0000",
            "rating": "5",
            "summary": "",
            "website": "www.website.com",
            "geocode": [51.5074889, -0.162236683080672],
            "apiPlaceId": "ADxmjKepdsfL"
        },
        2: {
            ...
        }
    }
    '''
    places_serial = {}

    for i, place_data in enumerate(places):

        place = place_schema.dump(place_data)
        place['id'] = place_data.id
        place['geocode'] = [place_data.lat, place_data.long]
        
        # making the index one of the keys with the place dictionary as the value
        places_serial[place['positionId']] = place

    return places_serial


def add_places(trip_id, places_arr):

    for i in range(len(places_arr)):

        place = places_arr[i]
        # if type(places_arr) == dict:
        #     place = places_arr[i + 1]

        # elif type(places_arr) == list:
        #     place = places_arr[i]

        apiId = place['apiId']
        position_id = place['positionId']
        name = place['name']
        address = place['address']
        img_url = place['imgUrl']
        info = place['info']
        favorite = place['favorite']
        category = place.get('category', None)
        phone_number = place.get('phoneNumber', None)
        rating = place.get('rating', None)
        summary = place.get('summary', None)
        website = place.get('website', None)
        avg_visit_time = place.get('avgVisitTime', 60)
        lat = place['lat']
        long = place['long']
        in_itinerary = False

        place = Place(apiId, position_id, name, address, img_url, 
                      info, favorite, category, phone_number, rating, summary, website, 
                      avg_visit_time, lat, long, in_itinerary, trip_id)

        db.session.add(place)
        db.session.commit()

def replace_day_id(places, day_id_1, day_id_2):
    # validate if theres any places in day
    if(places is None or len(places) <= 0):
        raise Exception(f'No places for day {day_id_1}')
    
    # update day id for each place
    for place in places:
        place.day_id = day_id_2
