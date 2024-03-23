from .models import Place

# finds the largest local_id in the list of places for that trip = places_last
def create_places_last(places):
    """
    places_last = the largest local_id in the list of places for that trip
    This function goes through a list of places and return that local_id
    """
    max_local_id = 0
    for place in places:
        local_id = place.local_id

        if local_id > max_local_id:
                max_local_id = local_id

    return max_local_id

def serialize_places(places, places_last):
    '''
    Serializes a list of Places, which creates a dictionary of places with the local_id as the key
    and the place data (a dict) as the value

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

        place['id'] = place_data.local_id
        place['place_id'] = place_data.place_id
        place['placeName'] = place_data.place_name
        place['info'] = place_data.info
        place['address'] = place_data.place_address
        place['imgURL'] = place_data.place_img
        place['lat'] = place_data.lat
        place['long'] = place_data.long
        place['favorite'] = place_data.favorite
        place['geocode'] = [place_data.lat, place_data.long]
        places_serial[place_data.local_id] = place


    result = []

    for i in range(places_last):
        place = places_serial[i + 1] 

        db_place = Place.query.filter_by(local_id = place['id'], trip_id = trip_id).first()

        places_serial[i + 1]['place_id'] = db_place.place_id

        result.append(place)