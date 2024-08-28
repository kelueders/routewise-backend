# EXTERNAL
from flask import Blueprint, request, jsonify
from datetime import timedelta

# INTERNAL
from ..models import Place, Trip, Day, db, place_schema
from .helpers import create_itinerary, add_places
from ..global_helpers import create_places_last, serialize_places
from .kmeans import Itinerary

itinerary = Blueprint('itinerary', __name__, url_prefix='/itinerary')

@itinerary.route('/createdays/<trip_id>', methods=['GET', 'PATCH'])
def create_days(trip_id):
    if not trip_id:
        return jsonify({'message': 'Trip ID is missing'}), 401
    
    places = Place.query.filter_by(trip_id = trip_id).all()

    # Finds the largest local_id in the list of places for that trip = places_last (type: int)
    places_last = create_places_last(places)

    trip = Trip.query.filter_by(trip_id = trip_id).first()
    if trip_id is None:
        return jsonify({'message': 'No Trip for trip ID'}), 404

    # Create days if they havent been created already
    days_data = Day.query.filter_by(trip_id = trip_id).all()
    days = {}
    if days_data is not None:
        # serialize days
        for i, day_data in enumerate(days_data):
            # serialize days
            day_id = f'day-{i + 1}'
            days[day_id] = {
                'id': day_id,
                'placeIds': [],
                'date_formatted': day_data.date_formatted,
                'date_converted': day_data.date_converted,
                'date_short': day_data.date_short,
                'day_short': day_data.week_day,
                'dayName': day_data.day_name
            } 
    else:
        current_date = trip.start_date
        for i in range(1, trip.duration + 1):
            # Day info
            date_converted = current_date.strftime('%A, %B %#d')
            date_short = current_date.strftime('%m/%d')
            week_day = current_date.strftime('%a')
            day_name = ""

            # Day dict
            day_id = f'day-{i}'
            days[day_id] = {
                'id': day_id,
                'placeIds': [],
                'date_formatted': current_date,
                'date_converted': date_converted,
                'date_short': date_short,
                'day_short': week_day,
                'dayName': day_name
            } 

            # Create and add day to database
            new_day = Day(current_date, date_converted, date_short, week_day, day_name, trip_id)
            db.session.add(new_day)

            # Increments by 1 the day that is added to the trip, starting at the trip start date
            current_date += timedelta(1)

    # Create Itinerary and cluster data
    itinerary = Itinerary(trip_id)
    itinerary_data = itinerary.cluster_analysis()       # 2D array - rows are days, columns are place_ids

    # Populate saved_places and days with places from itinerary_data
    saved_places_ids = []
    for i in range(len(itinerary_data)):
        for j in range(len(itinerary_data[i])):
            # Get place
            place_id = itinerary_data[i][j]
            place = Place.query.filter_by(local_id = place_id, trip_id = trip_id).first()

            days_day_id = f'day-{i+1}'
            if days_day_id in days:
                # Place is in an existing day
                # Add place_id to days
                day = days[days_day_id]
                new_day = Day.query.filter_by(date_formatted = day['date_formatted'], trip_id = trip_id).first()
                day['placeIds'].append(place_id)
                day['day_id'] = new_day.day_id

                # Add day_id to place, and set in_itinerary true
                place.day_id = new_day.day_id
                place.in_itinerary = True
                
            else:
                # Place is not in an existing day
                # Set day_id to None, and in_itinerary to false
                place.day_id = None
                place.in_itinerary = False

                # Add place_id to saved places
                saved_places_ids.append(place_id)

    # Update the trip 'is_itinerary' key to 'True'
    trip.is_itinerary = True
    db.session.commit()

    # Serializes the list of places (see global_helpers.py)
    serialized_places = serialize_places(Place.query.filter_by(trip_id = trip_id).all(), places_last, trip_id)
    # Remove local_id to coordinate with the front end
    for place_id in serialized_places:
        serialized_places[place_id]['id'] = serialized_places[place_id].pop('local_id') 
    
    # Packages the data in order to be rendered on the frontend
    return {
        "trip_id": trip_id,
        "places_last": places_last,
        "places": serialized_places,
        "days": days,
        "day_order": list(days.keys()),
        "saved_places": { "placesIds": saved_places_ids,
                        "addresses": list(map(lambda x: serialized_places[x]["address"], saved_places_ids))
                        }
    }

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

    if data['day_id']:
        day_id = data['day_id']
        in_itinerary = True
    else:
        day_id = None
        in_itinerary = False
    

    place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, info, favorite, 
                  category, phone_number, rating, summary, website, avg_visit_time, lat, long, in_itinerary, trip_id)
    
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

    
@itinerary.route('/move-day-places/<trip_id>', methods = ['PATCH'])
def move_day_places(trip_id):
    data = request.get_json()
    src_day_id = data['sourceDayId']
    dest_day_id = data['destDayId']
    swap = data['swap']

    try:
        # get all the places in the specified days
        src_places = Place.query.filter_by(trip_id = trip_id, day_id = src_day_id).all()
        dest_places = Place.query.filter_by(trip_id = trip_id, day_id = dest_day_id).all()

        # move places from source day to destination day
        replace_day_id(src_places, src_day_id, dest_day_id)
        
        if(swap):
            # move places from destination day to source day
            replace_day_id(dest_places, dest_day_id, src_day_id)

        db.session.commit()

        return "Successfully moved places", 200
    except Exception as e:
        return f'Failed: {e}', 502

def replace_day_id(places, day_id_1, day_id_2):
    # validate if theres any places in day
    if(places is None or len(places) <= 0):
        raise Exception(f'No places for day {day_id_1}')
    
    # update day id for each place
    for place in places:
        place.day_id = day_id_2