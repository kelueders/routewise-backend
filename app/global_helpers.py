from .models import Place, db, place_schema, Day, Trip
from datetime import timedelta

def serialize_places(places):
    places_serial = {}

    for i, place_data in enumerate(places):
        place = place_schema.dump(place_data)
        place['geocode'] = [place_data.lat, place_data.long]
        
        # making the index one of the keys with the place dictionary as the value
        places_serial[place['positionId']] = place
    return places_serial

def add_places(trip_id, places_arr):
    for i in range(len(places_arr)):
        place = places_arr[i]

        apiId = place['apiId']
        position_id = place['id']
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

def create_add_days(trip):
    days = {}
    current_date = trip.convert_to_datetime(trip.start_date)
    for i in range(1, trip.duration + 1):
        # Create and add day to database
        new_day = Day(i, '', current_date, trip.id)
        db.session.add(new_day)
        db.session.commit()

        # Serialize day
        day_dict = new_day.serialize(num=i, empty=True)
        days[day_dict['id']] = day_dict

        # Increments by 1 the day that is added to the trip, starting at the trip start date
        current_date += timedelta(1)
    return days

def replace_day_id(places, day_id_1, day_id_2):
    # validate if theres any places in day
    if(places is None or len(places) <= 0):
        raise Exception(f'No places for day {day_id_1}')
    
    # update day id for each place
    for place in places:
        place.day_id = day_id_2
