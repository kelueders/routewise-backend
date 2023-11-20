# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from app.models import Trip, db, trip_schema

places = Blueprint('places', __name__, url_prefix='/places')

# Create a new trip
@places.route('/trip', methods=['POST', 'GET'])
def add_trip():
    uid = request.json['uid']
    trip_name = request.json['tripName']
    destination = request.json['destination']
    img_url = request.json['destinationImgUrl']
    start_date = request.json['startDate']
    end_date = request.json['endDate']

    trip = Trip(trip_name, destination, img_url, start_date, end_date, uid)

    db.session.add(trip)
    db.session.commit()

    return f'It worked. Trip to {trip.destination} was created.'

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
# @places.route('/trips', methods = ['GET'])
# def get_trips(uid):

#     trips = Trip.query.filter_by(uid=user.uid)