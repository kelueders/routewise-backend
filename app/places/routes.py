# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from app.models import Trip, db

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

# Return a specific trip from the database to the front-end
# @places.route('/trip/<trip_id', methods=['GET'])