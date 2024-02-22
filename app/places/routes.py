# EXTERNAL
from flask import Blueprint, redirect, request, jsonify, url_for
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

            # data = place_schema.dump(place)
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

        # creates a dict of days with format:
        '''
        "days": {
            "day-1": {
                "id": "day-1",
                "date_converted": "Thursday, November 9",
                "day_short": "Thurs",
                "date_short": "11/9",
                "dayName": "",
                "placeIds": []
                NEED TO ADD REST OF THE DAY DATA *******
            }
        }
        '''
        days = {}

        # creates a list of day numbered labels in format: [day-1, day-2, day-3, ...]
        day_order = []    

        # creates a key in the days dict corresponding to "day-1", etc.  which contains data for that day
        for i, day in enumerate(days_db):
            days[f'day-{i + 1}'] = {
                'id': f'day-{i + 1}',
                'date_converted': day.date_converted,
                'day_short': day.week_day,
                'date_short': day.date_short,
                'dayName': day.day_name,
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
            "places": places_serial,
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
    
# Delete a trip
@places.route('/delete-trip/<trip_id>', methods = ['DELETE'])
def delete_trip(trip_id):

    if trip_id:
        trip = Trip.query.filter_by(trip_id = trip_id).first()
        places = Place.query.filter_by(trip_id = trip_id).all()
        days = Day.query.filter_by(trip_id = trip_id).all()

        print("Trip: ", trip)
        print("Places:", places)

        for place in places:
            db.session.delete(place)

        for day in days:
            db.session.delete(day)

        db.session.delete(trip)
        db.session.commit()

        return "Trip deleted"
    
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401
    
# Update a trip duration or name BEFORE the itinerary is created
@places.route('/update-trip-before/<trip_id>', methods = ['PATCH', 'POST'])
def update_trip_before(trip_id):

    trip = Trip.query.get(trip_id)

    data = request.get_json()

    print(data)

    if data['tripName']:
        trip.trip_name = data['tripName']     

    if data['startDate']:
        trip.start_date = data['startDate']
        trip.end_date = data['endDate']
        trip.duration = trip.calc_duration(trip.start_date, trip.end_date)

    db.session.commit()

    return "Trip Name and/or Duration Updated"

    
# Update a trip name and duration AFTER itinerary has already been created
@places.route('/update-trip/<trip_id>', methods = ['PATCH', 'POST'])
def update_trip(trip_id):

    trip = Trip.query.get(trip_id)

    data = request.get_json()

    print(data)

    if data['tripName']:
        trip.trip_name = data['tripName']     

    if data['startDate']:
        trip.start_date = data['startDate']
        trip.end_date = data['endDate']
        trip.duration = trip.calc_duration(trip.start_date, trip.end_date)

    db.session.commit()

    if data['startDate']:
        return redirect(url_for('itinerary.create_days', trip_id = trip_id))

    return "Trip Name and/or Duration Updated"


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
