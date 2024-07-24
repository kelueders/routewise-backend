# EXTERNAL
from flask import Blueprint, request, jsonify
from datetime import timedelta

# INTERNAL
from ..models import Place, Trip, Day, db, place_schema
from .helpers import create_itinerary, add_places
from ..global_helpers import create_places_last, serialize_places

itinerary = Blueprint('itinerary', __name__, url_prefix='/itinerary')

@itinerary.route('/createdays/<trip_id>', methods=['GET', 'PATCH'])
def create_days(trip_id):

    places = Place.query.filter_by(trip_id = trip_id).all()

    # finds the largest local_id in the list of places for that trip = places_last
    places_last = create_places_last(places)

    # Serializes the list of places (see global_helpers.py)
    serialized_places = serialize_places(places, places_last, trip_id)

    if trip_id:

        trip = Trip.query.filter_by(trip_id = trip_id).first()
        
        # Creates an itinerary for the trip, dividing the places into separate days - see itinerary/helpers.py
        trip_itinerary = create_itinerary(serialized_places, trip.duration)

        saved_places_ids = trip_itinerary['saved_places_ids']

        current_date = trip.start_date

        days = trip_itinerary['days']
        day_order = trip_itinerary['day_order']
        serialized_places = trip_itinerary['serialized_places']

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

        # db.session.commit()

        for day_num in day_order:
            day = days[day_num]

            new_day = Day.query.filter_by(date_formatted = day["date_formatted"], trip_id = trip_id).first()

            days[day_num]['day_id'] = new_day.day_id

            # looping through the places in the itinerary (excludes saved_places)
            for place_id in day['placeIds']:
                place = Place.query.filter_by(local_id = place_id, trip_id = trip_id).first()

                place.day_id = new_day.day_id
                place.in_itinerary = True
                serialized_places[place_id]['in_itinerary'] = True
            
                db.session.commit()

        for saved_place_id in saved_places_ids:
            serialized_places[saved_place_id]['in_itinerary'] = False

        # Assign the day_id to each place in the serialized_places object
        for i in range(places_last):
            place = serialized_places[i + 1] 

            db_place = Place.query.filter_by(local_id = place['local_id'], trip_id = trip_id).first()

            if db_place.day_id:
                serialized_places[i + 1]['day_id'] = db_place.day_id
            else:
                serialized_places[i + 1]['day_id'] = None

            # added so that it can coordinate with the front end, populates new 'id' key with 'local_id' then deletes the 'local_id' key
            serialized_places[i + 1]['id'] = serialized_places[i + 1].pop('local_id') 

        # update the trip 'is_itinerary' key to 'True' since an itinerary has now been created
        trip = Trip.query.filter_by(trip_id = trip_id).first()
        trip.is_itinerary = True

        db.session.commit()

        # packages the itinerary data in order to be rendered on the frontend
        itinerary_data = {
            "trip_id": trip_id,
            "places_last": places_last,
            "places": serialized_places,
            "days": days,
            "day_order": day_order,
            "saved_places": { "placesIds": saved_places_ids,
                            "addresses": list(map(lambda x: serialized_places[x]["address"], saved_places_ids))
                            }
        }
                
        return itinerary_data

    
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401

# When the user wants to add a place to a specific day in the trip when there is already an itinerary created    
@itinerary.route('/add-one-place/<trip_id>', methods = ['POST', 'GET'])
def add_one_place(trip_id):

    data = request.get_json()
    place = data['place']

    # print(place)

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

    if data['day_id']:
        day_id = data['day_id']
        in_itinerary = True
    else:
        day_id = None
        in_itinerary = False
    

    place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, 
                info, favorite, category, lat, long, in_itinerary, trip_id)
    
    # Why is this separate from the rest of the initialization?
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

    # print(data)

    place.day_id = data['day_id']
    if data['in_itinerary']:
        place.in_itinerary = True
    else:
        place.in_itinerary = False

    db.session.commit()

    return "Place Updated"

    # response = place_schema.dump(place)

    # return jsonify(response['place_id'])

    