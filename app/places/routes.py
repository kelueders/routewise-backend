# EXTERNAL
from flask import Blueprint, request, jsonify
from datetime import datetime

# INTERNAL
from ..models import Trip, Place, Day, db, trip_schema, trips_schema, places_schema, place_schema
from ..itinerary.helpers import add_places

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


    # ''' Calculates duration of the trip '''
    # # Determining duration of trip by converting string to datetime object
    # start_obj = datetime.strptime(start_date, '%m/%d/%Y').date()
    # end_obj = datetime.strptime(end_date, '%m/%d/%Y').date()

    # # then subtract and return type INT for days
    # duration = end_obj - start_obj
    # duration = duration.days + 1


    trip = Trip(trip_name, dest_city, dest_state, dest_country, dest_country_2letter, dest_lat, dest_long, 
                dest_url, start_date, end_date, uid)

    db.session.add(trip)
    db.session.commit()

    data = {
        "trip_id": trip.trip_id,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "duration": trip.duration
    }

    return data

    # return str(trip.trip_id)

    # return f'It worked. Trip to {trip.dest_city} was created.'

    # trip = Trip.query.filter_by(uid=trip.uid).first()

    # return trip_schema.jsonify(trip)

# Return a specific trip from the database to the front-end
@places.route('/trip/<trip_id>', methods=['GET'])
def get_trip(trip_id):

    if trip_id:

        # trip = Trip.query.filter_by(trip_id = trip_id).first()
        places = Place.query.filter_by(trip_id = trip_id).all()
        days_db = Day.query.filter_by(trip_id = trip_id).all()

        # finds the largest local_id in the list of places for that trip = places_last
        for place in places:
            max_local_id = 0
            local_id = place.local_id

            if local_id > max_local_id:
                max_local_id = local_id

        places_last = max_local_id

        # creates a dictionary with format:
        '''
        "places_serial: {
            "1": {
                ALL PLACE DATA
            },
            "2": {
                ALL PLACE DATA
            }
        }
        '''
        places_serial = {}

        for i, place in enumerate(places):

            data = place_schema.dump(place)

            places_serial[str(i + 1)] = data

        # creates a dict of days with format:
        '''
        "days": {
            "day-1": {
                "id": "day-1",
                "placeIds": []
                NEED TO ADD REST OF THE DAY DATA *******
            }
        }
        '''
        days = {}

        # creates a list of days numbered labels in format: [day-1, day-2, day-3, ...]
        day_order = []    

        for i, day in enumerate(days_db):
            days[f'day-{i + 1}'] = {
                'id': f'day-{i + 1}',
                'placeIds': []
            } 
            day_order.append(f'day-{i + 1}') 

            # adds the places for that day to the placeIds list of local_id 's
            places_in_day = Place.query.filter_by(trip_id = trip_id, day_id = day.day_id).all()

            for place in places_in_day:
                days[f'day-{i + 1}']['placeIds'].append(place.local_id)
            
        # final format of data to be sent to the front end    
        itinerary_data = {
            "trip_id": int(trip_id),
            "places_last": places_last,
            "places_serial": places_serial,
            "days": days,
            "day_order": day_order
        }

        return itinerary_data
    
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

    trip_id = request.json['tripId']
    places_last = request.json['placesLast']
    places_serial = request.json['places_serial']

    add_places(trip_id, places_last, places_serial)

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
