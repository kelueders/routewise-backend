# INTERNAL
from app.models import Place, db

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
            avg_visit_time = place.get('avg_visit_time', 60)
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
            avg_visit_time = place.get('avg_visit_time', 60)
            favorite = place['favorite']
            info = place['info']
            lat = place['lat']
            long = place['long']        

        place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, 
                      info, favorite, category, phone_number, rating, summary, website, avg_visit_time, lat, long, trip_id)

        db.session.add(place)
        db.session.commit()

