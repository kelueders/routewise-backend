from .models import Place

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
            "geocode": [51.5074889, -0.162236683080672]
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

        place['place_id'] = place_data.place_id
        place['info'] = place_data.info
        place['lat'] = place_data.lat
        place['long'] = place_data.long
        place['favorite'] = place_data.favorite
        place['geocode'] = [place_data.lat, place_data.long]

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