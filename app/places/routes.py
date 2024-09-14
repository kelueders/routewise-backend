# EXTERNAL
from flask import Blueprint, redirect, request, jsonify, url_for

# INTERNAL
from ..models import Trip, Place, Day, db, trip_schema, trips_schema, places_schema, place_schema
from ..global_helpers import create_day_dict, serialize_places, add_places

places = Blueprint('places', __name__, url_prefix='/places')

# Create a new trip
@places.route('/trip', methods=['POST', 'GET'])
def add_trip():
    # Get requested data
    uid = request.json['uid']
    trip_data = request.json['trip']

    trip_name = trip_data['name']
    city = trip_data['city']
    state = trip_data['state']
    country = trip_data['country']
    country_abbr = trip_data['countryAbbr']
    lat = trip_data['lat']
    long = trip_data['long']
    img_url = trip_data['imgUrl']
    start_date = trip_data['startDate']
    end_date = trip_data['endDate']

    # Create trip object
    trip = Trip(trip_name, city, state, country, country_abbr, lat, long, 
                img_url, start_date, end_date, uid)

    # Add trip to database
    db.session.add(trip)
    db.session.commit()

    # Validate and get new trip from database
    trip_record = Trip.query.filter_by(id=trip.id).first()
    if trip_record:
        return {
            "tripId": trip_record.id,
            "startDate": trip_record.start_date,
            "endDate": trip_record.end_date,
            "duration": trip_record.duration
        }, 200
    else:
        return jsonify({"message": "Failed to add trip"}), 500


# Return a specific trip from the database to the front-end
@places.route('/trip/<trip_id>', methods=['GET'])
def get_trip(trip_id):

    # Get all the necessary data
    places = Place.query.filter_by(trip_id=trip_id).all()
    day_records = Day.query.filter_by(trip_id=trip_id).all()
    if not places:
        return jsonify({"message": "No places associated with trip"}), 400
    
    serialized_places = serialize_places(places)

    # Create list of place ids that are not in the itinerary
    saved_places_ids = []
    for i, place_data in enumerate(places):
        if place_data.in_itinerary != True and not place_data.day_id:
            saved_places_ids.append(place_data.position_id)
    
    # Create a dict of days with keys "day-#"
    days = {}
    for i, day in enumerate(day_records):
        day_dict = create_day_dict(i + 1, day)
        days[day_dict['id']] = day_dict

        # Add the all the corresponding places id the day
        places_in_day = Place.query.filter_by(trip_id=trip_id, day_id=day.id).all()
        for place in places_in_day:
            days[day_dict['id']]['placeIds'].append(place.position_id)
        
    # Format of data to be sent to the front end
    return {
        "tripId": int(trip_id),
        "lastPlaceId": len(places),
        "places": serialized_places,
        "days": days,
        "dayOrder": list(days.keys()),
        "savedPlaces": { 
            "placesIds": saved_places_ids,
            "addresses": list(map(lambda x: serialized_places[x]["address"], saved_places_ids))
            }
        }, 200


# Return all the trips for a specific user   
@places.route('/trips/<uid>', methods=['GET'])
def get_trips(uid):
    # Get all trips from user
    trips = Trip.query.filter_by(uid=uid).all()
    if trips:
        response = trips_schema.dump(trips)
        return jsonify(response), 200
    else:
        return jsonify({"message": "No trips for user"}), 400


# Delete a trip and its corresponding places and days
@places.route('/delete-trip/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    
    # Get trip and corresponding places and days to delete
    trip = Trip.query.filter_by(id=trip_id).first()
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
    if (not Trip.query.filter_by(id=trip_id).first() and 
        not Place.query.filter_by(trip_id=trip_id).all() and 
        not Day.query.filter_by(trip_id=trip_id).all()):
        return jsonify({"message": "Trip deleted yay"}), 200
    else:
        return jsonify({"message": f"Failed to delete trip {trip_id}"}), 500


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
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return jsonify({"message": f"No trip {trip_id}"}), 400
    data = request.get_json()

    # Rename trip
    if data['tripName']:
        trip.name = data['tripName']  
        db.session.commit()

    # Edit trip dates
    if data['startDate'] or data['endDate']:
        if data['startDate']:
            trip.start_date = data['startDate']
        if data['endDate']:
            trip.end_date = data['endDate']
        # Update trip duration
        trip.duration = trip.calc_duration()
        db.session.commit()

        # If itinerary has been already been created, delete old days and create new itinerary
        if trip.is_itinerary:
            # delete old days
            days = Day.query.filter_by(trip_id=trip_id).all()
            for day in days:
                db.session.delete(day)
                
            db.session.commit()

            # create new itinerary
            return redirect(url_for('itinerary.create_days', trip_id=trip_id)), 200

    return jsonify({"message": "Trip Name and/or Duration Updated"}), 200


# Return all the places for a specific trip  
@places.route('/get-places/<trip_id>', methods=['GET'])
def get_places(trip_id):

    # Get places for trip
    places = Place.query.filter_by(trip_id=trip_id).all()
    if not places:
        return jsonify({"message": f"No places for trip {trip_id}"}), 400
    
    # Format places to send to frontend
    serialized_places = serialize_places(places)
    return serialized_places, 200


# Allows the user to add a place before there is an itinerary created, commit it to the database
# Also allows the user to add a place to the saved places list even after the itinerary is created
# and then return the place_id to the frontend
@places.route('add-place/<trip_id>', methods = ['GET', 'POST'])
def add_place(trip_id):

    # Get requested data about a place
    place_data = request.get_json()
    api_id = place_data['apiId']
    position_id = place_data['positionId']
    name = place_data['name']
    address = place_data['address']
    img_url = place_data['imgUrl']
    info = place_data['info']
    favorite = place_data['favorite']
    category = place_data.get('category', None)
    phone_number = place_data.get('phoneNumber', None)
    rating = place_data.get('rating', None)
    summary = place_data.get('summary', None)
    website = place_data.get('website', None)
    avg_visit_time = place_data.get('avgVisitTime', 60)
    lat = place_data['lat']
    long = place_data['long']
    in_itinerary = False

    place = Place(api_id, position_id, name, address, img_url, info, favorite, 
                  category, phone_number, rating, summary, website, avg_visit_time, lat, long, in_itinerary, trip_id)

    db.session.add(place)
    db.session.commit()

    # Validate that the place has been added and return place id
    place_record = Place.query.filter_by(position_id=position_id, trip_id=trip_id).first()
    if place_record:
        return str(place_record.api_id), 200
    else:
        return jsonify({"message": "Place could not be added"}), 500


# User flow for when the user is not logged in - it will create the trip and places at the same time
@places.route('add-trip-and-places', methods=['GET', 'POST'])
def add_trip_and_places():

    # Get requested data about trip
    data = request.get_json()

    uid = data['uid']
    trip_data = data['trip']
    trip_name = trip_data['name']
    city = trip_data['city']
    state = trip_data['state']
    country = trip_data['country']
    country_abbr = trip_data['countryAbbr']
    lat = trip_data['geocode'][0]
    long = trip_data['geocode'][1]
    img_url = trip_data['imgUrl']
    start_date = trip_data['startDate']
    end_date = trip_data['endDate']

    # Create and add Trip to database
    trip = Trip(trip_name, city, state, country, country_abbr, lat, long, 
            img_url, start_date, end_date, uid)
    
    db.session.add(trip)
    db.session.commit()

    # Get places data
    places = trip_data['places']
    places_last_id = len(places) + 1

    # Create and add places to database
    add_places(trip.id, places_last_id, places)

    # Validate trip and places were added successfully
    trip_record = Trip.query.filter_by(id=trip.id)
    place_records = Place.query.filter_by(trip_id=trip.id).all()
    if trip_record and (len(place_records) == len(places)):
        return jsonify({"message": "Trip and places have been added to the database."}), 200
    else:
        return jsonify({"message": "Failed adding trip or places"}), 500
