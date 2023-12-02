# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from app.models import Trip, Place, db, trip_schema, trips_schema, places_schema

places = Blueprint('places', __name__, url_prefix='/places')

# Create a new trip
@places.route('/trip', methods=['POST', 'GET'])
def add_trip():
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

    trip = Trip(trip_name, dest_city, dest_state, dest_country, dest_country_2letter, dest_lat, dest_long, 
                dest_url, start_date, end_date, uid)

    db.session.add(trip)
    db.session.commit()

    return str(trip.trip_id)

    # return f'It worked. Trip to {trip.dest_city} was created.'

    # trip = Trip.query.filter_by(uid=trip.uid).first()

    # return trip_schema.jsonify(trip)

# Return a specific trip from the database to the front-end
@places.route('/trip/<trip_id>', methods=['GET'])
def get_trip(trip_id):

    if trip_id:
        trip = Trip.query.get(trip_id)
        response = trip_schema.dump(trip)
        return jsonify(response)
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401
    
    
# Return all the trips for a specific user   
@places.route('/trips/<uid>', methods = ['GET'])
def get_trips(uid):

    if uid:
        trips = Trip.query.filter_by(uid = uid).all()
        response = trips_schema.dump(trips)
        return jsonify(response)
    else:
        return jsonify({'message': 'UID is missing'}), 401


# Add a place to the user's list
@places.route('/place', methods=['POST'])
def add_place():

    trip_id = request.json['tripID']
    data = request.json['places']

    for place in data:

        place_name = place['placeName']
        geoapify_placeId = place['placeId']
        place_address = place['address']
        place_img = place['imgURL']
        category = place['category']
        favorite = place['favorite']
        info = place['info']
        lat = place['lat']
        long = place['long']

        place = Place(place_name, geoapify_placeId, place_address, place_img, 
                      info, favorite, category, lat, long, trip_id)

        db.session.add(place)
        db.session.commit()

    return "It worked. The places were added!"


# Return all the places for a specific trip  
@places.route('/places/<trip_id>', methods = ['GET'])
def get_places(trip_id):

    if trip_id:
        places = Place.query.filter_by(trip_id = trip_id).all()
        response = places_schema.dump(places)
        print(response)
        return jsonify(response)
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401
