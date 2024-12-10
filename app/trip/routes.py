# EXTERNAL
from flask import Blueprint, redirect, request, jsonify, url_for

# INTERNAL
from ..models import Trip, Place, Day, db, trips_schema
from ..global_helpers import serialize_places, add_places, create_add_days

trip = Blueprint('trip', __name__, url_prefix='/trip')


# Create a new trip
@trip.route('/add', methods=['POST'])
def create_trip():

    uid = request.json['uid']
    trip_data = request.json['trip']

    trip_name = trip_data['name']
    city = trip_data['city']
    state = trip_data['state']
    country = trip_data['country']
    country_abbr = trip_data['countryAbbr']
    img_url = trip_data['imgUrl']
    start_date = trip_data['startDate']
    end_date = trip_data['endDate']

    if 'lat' in trip_data:
        lat = trip_data['lat']
        long = trip_data['long']
    elif 'geocode' in trip_data:
        lat = trip_data['geocode'][0]
        long = trip_data['geocode'][1]

    # Create trip object
    trip = Trip(trip_name, city, state, country, country_abbr, lat, long, 
                img_url, start_date, end_date, uid)

    # Add trip to database
    db.session.add(trip)
    db.session.commit()

    # Create days and add to database
    create_add_days(trip)

    # Get places data
    if 'places' in trip_data:
        places = trip_data['places']
        # Create and add places to database
        add_places(trip.id, places)

        # Validate places were added successfully
        place_records = Place.query.filter_by(trip_id=trip.id).all()
        if len(place_records) != len(places):
            return jsonify({"message": "Failed to add places"}), 500

    # Validate and get new trip from database
    if trip.id:
        return {
            "tripId": trip.id,
            "startDate": trip.start_date,
            "endDate": trip.end_date,
            "duration": trip.duration
        }, 200
    else:
        return jsonify({"message": "Failed to add trip"}), 500


# Return a specific trip from the database to the front-end
@trip.route('/<trip_id>', methods=['GET'])
def get_trip(trip_id):

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
        day_dict = day.serialize(num=i+1, empty=False)
        days[day_dict['id']] = day_dict
        
    # Format of data to be sent to the front end
    return {
        "tripId": int(trip_id),
        "lastPlaceId": places[-1].position_id,
        "places": serialized_places,
        "days": days,
        "dayOrder": list(days.keys()),
        "savedPlaces": { 
            "placesIds": saved_places_ids,
            "addresses": list(map(lambda x: serialized_places[x]["address"], saved_places_ids))
            }
        }, 200


# Return all the trips for a specific user   
@trip.route('/trips/<uid>', methods=['GET'])
def get_trips(uid):

    # Get all trips from user
    trips = Trip.query.filter_by(uid=uid).all()
    if trips:
        response = trips_schema.dump(trips)
        return jsonify(response), 200
    else:
        return jsonify({"message": "No trips for user"}), 400
    

# Delete a trip and its corresponding places and days
@trip.route('/delete/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    
    # Get trip and corresponding places and days to delete
    trip = Trip.query.filter_by(id=trip_id).first()
    places = trip.place
    days = trip.day

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
@trip.route('/update/<trip_id>', methods=['PATCH', 'POST', 'DELETE'])
def update_trip(trip_id):

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
        
        # delete old days and recreate them
        days = trip.day
        for day in days:
            db.session.delete(day)
        db.session.commit()
        create_add_days(trip)

        # If itinerary has been already been created, recreate a new itinerary
        if trip.is_itinerary:
            return redirect(url_for('itinerary.generate_itinerary', trip_id=trip_id))

    return jsonify({"message": "Trip Name and/or Duration Updated"}), 200