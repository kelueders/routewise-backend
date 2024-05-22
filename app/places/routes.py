# EXTERNAL
from flask import Blueprint, redirect, request, jsonify, url_for
from datetime import datetime

# INTERNAL
from ..models import Trip, Place, Day, db, trip_schema, trips_schema, places_schema, place_schema
from ..itinerary.helpers import add_places
from ..global_helpers import create_places_last, serialize_places

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


# Return a specific trip from the database to the front-end
@places.route('/trip/<trip_id>', methods=['GET'])
def get_trip(trip_id):

    if trip_id:

        # trip = Trip.query.filter_by(trip_id = trip_id).first()
        places = Place.query.filter_by(trip_id = trip_id).all()
        days_db = Day.query.filter_by(trip_id = trip_id).all()

        # finds the largest local_id in the list of places for that trip = places_last
        places_last = create_places_last(places)

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
                'db_id': day.day_id,
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

        return "Trip deleted yay"
    
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401

'''
** Update a Trip Name AND/OR Date **
- will be used in 3 places:
    - Dashboard page - can update trip name and dates, is_itinerary = True or False
    - Places List page - can update trip dates, is_itinerary = True or False
    - Itinerary page - can update trip dates, is_itinerary = True
'''
@places.route('/update-trip/<trip_id>', methods = ['PATCH', 'POST', 'GET', 'DELETE'])
def update_trip(trip_id):

    trip = Trip.query.get(trip_id)

    data = request.get_json()

    print(data)

    if data['tripName']:
        trip.trip_name = data['tripName']  

    if data['startDate'] or data['endDate']:
        if data['startDate']:
            trip.start_date = data['startDate']
        if data['endDate']:
            trip.end_date = data['endDate']
        trip.duration = trip.calc_duration(trip.start_date, trip.end_date)

        db.session.commit()

        if trip.is_itinerary:
            days = Day.query.filter_by(trip_id = trip_id).all()

            for day in days:
                db.session.delete(day)
                
            db.session.commit()

            return redirect(url_for('itinerary.create_days', trip_id = trip_id))

        # the itinerary has not been updated because there is no itinerary yet
        return "Itinerary not updated, dates were changed"

    db.session.commit()

    # if there IS an itinerary already created do this
    if trip.is_itinerary:
        return redirect(url_for('itinerary.create_days', trip_id=trip_id))


    return "Trip Name and/or Duration Updated"


# Add a place to the user's list
@places.route('/add-place/<trip_id>', methods=['POST'])
def add_place(trip_id):

    trip_id = request.json['tripId']
    places_last = request.json['placesLast']
    places_serial = request.json['places_serial']

    add_places(trip_id, places_last, places_serial)

    return "It worked. The places were added!"


# Return all the places for a specific trip  
@places.route('/get-places/<trip_id>', methods = ['GET'])
def get_places(trip_id):

    if trip_id:
        places = Place.query.filter_by(trip_id = trip_id).all()
        response = places_schema.dump(places)
        print(response)
        return jsonify(response)
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401
    
# allows the user to add a place, commit it to the database, and then return the place_id to the front
@places.route('add-get-place/<trip_id>', methods = ['GET', 'POST'])
def add_get_place(trip_id):

    place = request.get_json()

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
    in_itinerary = place['in_itinerary']

    place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, 
                    info, favorite, category, lat, long, in_itinerary, trip_id)

    db.session.add(place)
    db.session.commit()

    place = Place.query.filter_by(local_id = local_id, trip_id = trip_id).first()

    response = place_schema.dump(place)

    return jsonify(response['place_id'])

# user flow for when the user is not logged in - it will create the trip and places at the same time
@places.route('add-trip-and-places/', methods = ['GET', 'POST'])
def add_trip_and_places():

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

    trip = Trip(trip_name, dest_city, dest_state, dest_country, dest_country_2letter, dest_lat, dest_long, 
            dest_url, start_date, end_date, uid)
    
    db.session.add(trip)
    db.session.commit()

    places = trip_data['places']

    places_last = create_places_last(places)
    # places_serial = serialize_places(places, places_last, trip.trip_id)

    add_places(trip.trip_id, places_last, places)

    return "Trip and places have been added to the database."

