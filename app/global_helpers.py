from .models import Place, db

# finds the largest local_id in the list of places for that trip = places_last
def create_places_last(places):
    """
    places_last = the largest local_id in the list of places for that trip
    This function goes through a list of places and return that local_id
    """
    max_local_id = 0
    local_id = 0
    for place in places:
        if hasattr(place, 'id'):
            local_id = place.id
        elif hasattr(place, 'local_id'):
            local_id = place.local_id

        if local_id > max_local_id:
                max_local_id = local_id

    return max_local_id

def serialize_places(places, places_last, trip_id):
    '''
    Serializes a list of Places.
        Returns a dictionary with  that each have a local_id as the KEY and the 
        place data (a dict) as the VALUE for each place

    {
        1: {
            "local_id": 1,
            "placeName": "Hyde Park",
            "address": "Hyde Park, Albion Street, London, W2 2LG, United Kingdom",
            "imgURL": "https://images.unsplash.com/",
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

        place = {}

        place['id'] = place_data.id
        place['apiId'] = place_data.api_id
        place['positionId'] = place_data.position_id
        place['name'] = place_data.name
        place['address'] = place_data.address
        place['imgUrl'] = place_data.img_url
        place['info'] = place_data.info
        place['favorite'] = place_data.favorite
        place['category'] = place_data.category
        place['phoneNumber'] = place_data.phone_number
        place['rating'] = place_data.rating
        place['summary'] = place_data.summary
        place['website'] = place_data.website
        place['avgVisitTime'] = place_data.avg_visit_time
        place['geocode'] = [place_data.lat, place_data.long]
        place['lat'] = place_data.lat
        place['long'] = place_data.long

        if hasattr(place_data, 'day_id'):
            place['dayId'] = place_data.day_id
        if hasattr(place_data, 'in_itinerary'):
            place['inItinerary'] = place_data.in_itinerary
        
        # making the index one of the keys with the place dictionary as the value
        places_serial[place['positionId']] = place

    # for i in range(places_last):

    #     # extracts the places_serial dictionary (the value) at the corresponding serial number key.
    #     place = places_serial[i + 1] 

    #     db_place = Place.query.filter_by(position_id=place['positionId'], trip_id=trip_id).first()

    #     # Are we repeating the assigning of the 'place_id' key because the first object originally fed into 
    #     # the function may not always have the place_id?
    #     # Like if the places are coming from the frontend and have not been inputted in the database yet?
    #     places_serial[i + 1]['place_id'] = db_place.place_id

    return places_serial


def add_places(trip_id, places_last_id, places_arr):

    for i in range(places_last_id):

        if type(places_arr) == dict:
            place = places_arr[i + 1]

        elif type(places_arr) == list:
            place = places_arr[i]

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

def create_day_dict(day_num, day):
    id = f'day-{day_num}'
    return {
        'id': id,
        'dayId': day.day_id,
        'placeIds': [],
        'dateFormatted': day.date_formatted,
        'dateConverted': day.date_converted,
        'dateShort': day.date_short,
        'dayShort': day.week_day,
        'dayName': day.day_name
    }