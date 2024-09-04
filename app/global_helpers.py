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

        if hasattr(place_data, 'local_id'):
            place['local_id'] = place_data.local_id
            place['placeName'] = place_data.place_name
            place['address'] = place_data.place_address
            place['imgURL'] = place_data.place_img
        elif hasattr(place_data, 'id'):
            place['local_id'] = place_data.id
            place['placeName'] = place_data.placeName
            place['address'] = place_data.address
            place['imgURL'] = place_data.imgURL

        if hasattr(place_data, 'day_id'):
            place['day_id'] = place_data.day_id
        if hasattr(place_data, 'in_itinerary'):
            place['in_itinerary'] = place_data.in_itinerary

        place['place_id'] = place_data.place_id
        place['info'] = place_data.info
        place['lat'] = place_data.lat
        place['long'] = place_data.long
        place['favorite'] = place_data.favorite
        place['category'] = place_data.category
        place['phoneNumber'] = place_data.phone_number
        place['rating'] = place_data.rating
        place['summary'] = place_data.summary
        place['website'] = place_data.website
        place['avgVisitTime'] = place_data.avg_visit_time
        place['geocode'] = [place_data.lat, place_data.long]
        place['apiPlaceId'] = place_data.geoapify_placeId

        # making the local_id one of the keys with the place dictionary as the value
        places_serial[place['local_id']] = place

    for i in range(places_last):

        # extracts the places_serial dictionary (the value) at the corresponding serial number key.
        place = places_serial[i + 1] 

        db_place = Place.query.filter_by(local_id = place['local_id'], trip_id = trip_id).first()

        # Are we repeating the assigning of the 'place_id' key because the first object originally fed into 
        # the function may not always have the place_id?
        # Like if the places are coming from the frontend and have not been inputted in the database yet?
        places_serial[i + 1]['place_id'] = db_place.place_id

    return places_serial


def add_places(trip_id, places_last, places_arr):

    for i in range(places_last):

        if type(places_arr) == dict:
            place = places_arr[i + 1]
            
            local_id = place['local_id']
            place_name = place['placeName']
            geoapify_placeId = place['placeId']
            place_address = place['address']
            place_img = place['imgURL']
            favorite = place['favorite']            
            category = place.get('category', None)
            phone_number = place.get('phoneNumber', None)
            rating = place.get('rating', None)
            summary = place.get('summary', None)
            website = place.get('website', None)
            avg_visit_time = place.get('avgVisitTime', 60)
            info = place['info']
            lat = place['lat']
            long = place['long']   

        elif type(places_arr) == list:
            place = places_arr[i]

            local_id = place['id']
            place_name = place['placeName']
            geoapify_placeId = place['place_id']
            place_address = place['address']
            place_img = place['imgURL']
            category = place.get('category', None)
            phone_number = place.get('phoneNumber', None)
            rating = place.get('rating', None)
            summary = place.get('summary', None)
            website = place.get('website', None)
            avg_visit_time = place.get('avgVisitTime', 60)
            favorite = place['favorite']
            info = place['info']
            lat = place['lat']
            long = place['long']        

        place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, 
                      info, favorite, category, phone_number, rating, summary, website, avg_visit_time, lat, long, trip_id)

        db.session.add(place)
        db.session.commit()

def replace_day_id(places, day_id_1, day_id_2):
    # validate if theres any places in day
    if(places is None or len(places) <= 0):
        raise Exception(f'No places for day {day_id_1}')
    
    # update day id for each place
    for place in places:
        place.day_id = day_id_2