from .models import Place

# finds the largest local_id in the list of places for that trip = places_last
def create_places_last(places):
    """
    places_last = the largest local_id in the list of places for that trip
    This function goes through a list of places and return that local_id
    """
    max_local_id = 0
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
        Creates a list of dictionaries that each have a local_id as the KEY and the 
        place data (a dict) as the VALUE for each place

    places_serial = {
        1: {
            id:
            place_id:
            placeName:
            info:
            address:
            imgURL:
            lat:
            long:
            favorite:
            geocode:
        },
        2: {
            ALL PLACE DATA
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

        places_serial[place['local_id']] = place

    for i in range(places_last):
        place = places_serial[i + 1] 

        db_place = Place.query.filter_by(local_id = place['local_id'], trip_id = trip_id).first()

        places_serial[i + 1]['place_id'] = db_place.place_id

    return places_serial