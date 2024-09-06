# EXTERNAL
from flask import Blueprint, redirect, request, jsonify, url_for

# INTERNAL
from ..models import Trip, Place, Day, db, trip_schema, trips_schema, places_schema, place_schema
from ..global_helpers import create_places_last, serialize_places, add_places, create_day_dict

places = Blueprint('places', __name__, url_prefix='/places')

# Create a new trip
@places.route('/trip', methods=['POST', 'GET'])
def add_trip():
    # Get requested data
    uid = request.json['uid']
    trip_data = request.json['tripData']

    trip_name = trip_data['tripName']
    dest_city = trip_data['cityName']
    dest_state = trip_data['state']
    dest_country = trip_data['country']
    dest_country_2letter = trip_data['country_2letter']
    dest_lat = trip_data['destinationLat']
    dest_long = trip_data['destinationLong']
    dest_url = trip_data['destinationImg']
    start_date = trip_data['startDate']
    end_date = trip_data['endDate']

    # Create trip object
    trip = Trip(trip_name, dest_city, dest_state, dest_country, dest_country_2letter, dest_lat, dest_long, 
                dest_url, start_date, end_date, uid)

    # Add trip to database
    db.session.add(trip)
    db.session.commit()

    # Validate and get new trip from database
    trip_record = Trip.query.filter_by(trip_id=trip.trip_id).first()
    if trip_record:
        return {
            "trip_id": trip_record.trip_id,
            "start_date": trip_record.start_date,
            "end_date": trip_record.end_date,
            "duration": trip_record.duration
        }, 200
    else:
        return "Failed to add trip", 500


# Return a specific trip from the database to the front-end
@places.route('/trip/<trip_id>', methods=['GET'])
def get_trip(trip_id):

    if not trip_id:
        return jsonify({'message': 'Trip ID is missing'}), 401

    # Get all the necessary data
    places = Place.query.filter_by(trip_id=trip_id).all()
    day_records = Day.query.filter_by(trip_id=trip_id).all()
    if not places or not day_records:
        return jsonify({'message': 'No places or days associated with trip'}), 400
    
    places_last_id = create_places_last(places)
    serialized_places = serialize_places(places, places_last_id, trip_id)

    # Create list of place ids that are not in the itinerary
    saved_places_ids = []
    for i, place_data in enumerate(places):
        if place_data.in_itinerary != True and not place_data.day_id:
            saved_places_ids.append(place_data.local_id)
    
    # Create a dict of days with keys "day-#"
    days = {}
    for i, day in enumerate(day_records):
        day_dict = create_day_dict(i+1, day)
        days[day_dict['id']] = day_dict
        # day_id = f'day-{i + 1}'
        # days[day_id] = {
        #     'id': day_id,
        #     'day_id': day.day_id,
        #     'placeIds': [],
        #     'date_formatted': day.date_formatted,
        #     'date_converted': day.date_converted,
        #     'date_short': day.date_short,
        #     'day_short': day.week_day,
        #     'dayName': day.day_name
        # } 

        # Add the all the corresponding places id the day
        places_in_day = Place.query.filter_by(trip_id=trip_id, day_id=day.day_id).all()
        for place in places_in_day:
            days[day_dict['id']]['placeIds'].append(place.local_id)
        
    # Format of data to be sent to the front end
    return {
        "trip_id": int(trip_id),
        "places_last": places_last_id,
        "places": serialized_places,
        "days": days,
        "day_order": list(days.keys()),
        "saved_places": { 
            "placesIds": saved_places_ids,
            "addresses": list(map(lambda x: serialized_places[x]["address"], saved_places_ids))
            }
        }, 200


# Return all the trips for a specific user   
@places.route('/trips/<uid>', methods=['GET'])
def get_trips(uid):
    if not uid:
        return jsonify({'message': 'UID is missing'}), 401

    # Get all trips from user
    trips = Trip.query.filter_by(uid=uid).all()
    if trips:
        response = trips_schema.dump(trips)
        return jsonify(response), 200
    else:
        return jsonify({'message': 'No user'}), 400


# Delete a trip and its corresponding places and days
@places.route('/delete-trip/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    if not trip_id:
        return jsonify({'message': 'Trip ID is missing'}), 401
    
    # Get trip and corresponding places and days to delete
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    places = Place.query.filter_by(trip_id=trip_id).all()
    days = Day.query.filter_by(trip_id=trip_id).all()

    # Delete each place in trip
    for place in places:
        db.session.delete(place)

    # Delete each day in trip
    for day in days:
        db.session.delete(day)

    # Update database
    db.session.delete(trip)
    db.session.commit()

    # Validate data has been deleted
    if (not Trip.query.filter_by(trip_id=trip_id).first() and 
        not Place.query.filter_by(trip_id=trip_id).all() and 
        not Day.query.filter_by(trip_id=trip_id).all()):
        return "Trip deleted yay", 200
    else:
        return f"Failed to delete trip {trip_id}", 500


'''
** Update a Trip Name AND/OR Date **
- will be used in 3 places:
    - Dashboard page - can update trip name and dates, is_itinerary = True or False
    - Places List page - can update trip dates, is_itinerary = True or False
    - Itinerary page - can update trip dates, is_itinerary = True
'''
@places.route('/update-trip/<trip_id>', methods=['PATCH', 'POST', 'GET', 'DELETE'])
def update_trip(trip_id):

    # Get requested data
    trip = Trip.query.get(trip_id)
    if not trip:
        return f"No trip {trip_id}", 400
    data = request.get_json()

    # Rename trip
    if data['tripName']:
        trip.trip_name = data['tripName']  
        db.session.commit()

    # Edit trip dates
    if data['startDate'] or data['endDate']:
        if data['startDate']:
            trip.start_date = data['startDate']
        if data['endDate']:
            trip.end_date = data['endDate']
        # Update trip duration
        trip.duration = trip.calc_duration(trip.start_date, trip.end_date)
        db.session.commit()

        # If itinerary has been already been created, delete old days and create new itinerary
        if trip.is_itinerary:
            print("shouldnt be getting here")
            # delete old days
            days = Day.query.filter_by(trip_id=trip_id).all()
            for day in days:
                db.session.delete(day)
                
            db.session.commit()

            # create new itinerary
            return redirect(url_for('itinerary.create_days', trip_id=trip_id))

    return "Trip Name and/or Duration Updated", 200


# Return all the places for a specific trip  
@places.route('/get-places/<trip_id>', methods=['GET'])
def get_places(trip_id):

    if not trip_id:
        return jsonify({'message': 'Trip ID is missing'}), 401
    
    # Get places for trip
    places = Place.query.filter_by(trip_id=trip_id).all()
    if not places:
        return f"No places for trip {trip_id}", 400
    
    # Format places to send to frontend
    places_last_id = create_places_last(places)
    serialized_places = serialize_places(places, places_last_id, trip_id)
    return serialized_places, 200


# Allows the user to add a place before there is an itinerary created, commit it to the database
# Also allows the user to add a place to the saved places list even after the itinerary is created
# and then return the place_id to the frontend
@places.route('add-place/<trip_id>', methods = ['GET', 'POST'])
def add_place(trip_id):

    # Get requested data about a place
    place_data = request.get_json()
    local_id = place_data['id']
    place_name = place_data['placeName']
    geoapify_placeId = place_data['placeId']
    place_address = place_data['address']
    place_img = place_data['imgURL']
    category = place_data.get('category', None)
    phone_number = place_data.get('phoneNumber', None)
    rating = place_data.get('rating', None)
    summary = place_data.get('summary', None)
    website = place_data.get('website', None)
    avg_visit_time = place_data.get('avgVisitTime', 60)
    favorite = place_data['favorite']
    info = place_data['info']
    lat = place_data['lat']
    long = place_data['long']
    in_itinerary = False

    place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, info, favorite, 
                  category, phone_number, rating, summary, website, avg_visit_time, lat, long, in_itinerary, trip_id)

    db.session.add(place)
    db.session.commit()

    # Validate that the place has been added and return place id
    place_record = Place.query.filter_by(local_id=local_id, trip_id=trip_id).first()
    if place_record:
        return str(place_record.place_id), 200
    else:
        return "Place could not be added", 500


# User flow for when the user is not logged in - it will create the trip and places at the same time
@places.route('add-trip-and-places/', methods=['GET', 'POST'])
def add_trip_and_places():

    # Get requested data about trip
    data = request.get_json()

    uid = data['uid']
    trip_data = data['currentTrip']
    trip_name = trip_data['tripName']
    dest_city = trip_data['city']
    dest_state = trip_data['state']
    dest_country = trip_data['country']
    dest_country_2letter = trip_data['country_2letter']
    dest_lat = trip_data['geocode'][0]
    dest_long = trip_data['geocode'][1]
    dest_url = trip_data['imgUrl']
    start_date = trip_data['startDate']
    end_date = trip_data['endDate']

    # Create and add Trip to database
    trip = Trip(trip_name, dest_city, dest_state, dest_country, dest_country_2letter, dest_lat, dest_long, 
            dest_url, start_date, end_date, uid)
    
    db.session.add(trip)
    db.session.commit()

    # Get places data
    places = trip_data['places']
    places_last_id = create_places_last(places)

    # Create and add places to database
    add_places(trip.trip_id, places_last_id, places)

    # Validate trip and places were added successfully
    trip_record = Trip.query.filter_by(trip_id=trip.trip_id)
    place_records = Place.query.filter_by(trip_id=trip.trip_id).all()
    if trip_record and (create_places_last(place_records) == (places_last_id + len(places))):
        return "Trip and places have been added to the database.", 200
    else:
        return "Failed adding trip or places", 500
