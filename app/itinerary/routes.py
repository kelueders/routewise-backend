# EXTERNAL
from flask import Blueprint, request, jsonify
from datetime import timedelta

# INTERNAL
from ..models import Place, Trip, Day, db, place_schema
from .helpers import create_itinerary, add_places

itinerary = Blueprint('itinerary', __name__, url_prefix='/itinerary')

@itinerary.route('/createdays/<trip_id>', methods=['GET'])
def create_days(trip_id):

    places = Place.query.filter_by(trip_id = trip_id).all()

    # finds the largest local_id in the list of places for that trip = places_last
    max_local_id = 0
    for place in places:
        local_id = place.local_id

        if local_id > max_local_id:
            max_local_id = local_id

    places_last = max_local_id

    # creates a dictionary with format:
    '''
    "places_serial: {
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


    add_places(trip_id, places_last, places_serial)

    result = []

    for i in range(places_last):
        place = places_serial[i + 1] 

        db_place = Place.query.filter_by(local_id = place['id'], trip_id = trip_id).first()

        places_serial[i + 1]['place_id'] = db_place.place_id

        result.append(place)

    if trip_id:
        # places = Place.query.filter_by(trip_id = trip_id).all()
        # result = places_schema.dump(places)
        # jsonify(result)

        trip = Trip.query.filter_by(trip_id = trip_id).first()
        
        day_data = create_itinerary(result, trip.duration)

        current_date = trip.start_date

        days = day_data['days']
        day_order = day_data['day_order']

        for day_num in day_order:
            day = days[day_num]

            date_short = current_date.strftime('%m/%d')
            week_day = current_date.strftime('%a')
            date_converted = current_date.strftime('%A, %B %#d')
            day_name = ""

            new_day = Day(current_date, date_converted, date_short, week_day, day_name, trip_id)

            db.session.add(new_day)

            day["date_formatted"] = current_date
            day["date_converted"] = date_converted
            day["date_short"] = date_short
            day["day_short"] = week_day
            day_name = ""

            current_date += timedelta(1)       # increments by 1 the day that is added to the trip, starting at the trip start date

        db.session.commit()

        for day_num in day_order:
            day = days[day_num]

            new_day = Day.query.filter_by(date_formatted = day["date_formatted"], trip_id = trip_id).first()

            days[day_num]['day_id'] = new_day.day_id

            for place_id in day['placeIds']:
                place = Place.query.filter_by(local_id = place_id, trip_id = trip_id).first()

                place.day_id = new_day.day_id
            
                db.session.commit()

        # Assign the day_id to each place in the places_serial object
        for i in range(places_last):
            place = places_serial[i + 1] 

            db_place = Place.query.filter_by(local_id = place['id'], trip_id = trip_id).first()

            places_serial[i + 1]['day_id'] = db_place.day_id

        # update the trip 'is_itinerary' key to 'True' since an itinerary has now been created
        trip = Trip.query.filter_by(trip_id = trip_id).first()
        trip.is_itinerary = True

        # packages the itinerary data in order to be rendered on the frontend
        itinerary_data = {
            "trip_id": trip_id,
            "places_last": places_last,
            "places": places_serial,
            "days": days,
            "day_order": day_order
        }
                
        return itinerary_data

    
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401
    
@itinerary.route('/add-one-place/<trip_id>', methods = ['POST', 'GET'])
def add_one_place(trip_id):

    data = request.get_json()
    place = data['place']

    print(place)

    local_id = place['id']
    place_name = place['placeName']
    geoapify_placeId = place['placeId']
    place_address = place['address']
    place_img = place['imgURL']
    category = place['category']
    favorite = place['favorite']
    info = place['info']
    lat = place['lat']
    long = place['long']
    day_id = data['day_id']
    

    place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, 
                info, favorite, category, lat, long, trip_id)
    
    place.update_day_id(day_id)

    db.session.add(place)
    db.session.commit()

    #### NEED TO RETURN THE place_id to the front end
    place = Place.query.filter_by(local_id = local_id, trip_id = trip_id).first()

    response = place_schema.dump(place)

    return jsonify(response['place_id'])


@itinerary.route('/delete-place/<place_id>', methods = ['DELETE'])
def delete_place(place_id):

    place = Place.query.get(place_id)
    
    db.session.delete(place)
    db.session.commit()

    return "Place deleted"


@itinerary.route('/update-place/<place_id>', methods = ['PATCH'])
def update_place(place_id):

    place = Place.query.get(place_id)

    data = request.get_json()

    print(data)

    place.day_id = data['day_id']

    db.session.commit()

    return "Place Updated"

    # response = place_schema.dump(place)

    # return jsonify(response['place_id'])

    