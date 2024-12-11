# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from ..models import Trip, Place, db
from ..global_helpers import serialize_places, replace_day_id, add_places, create_add_days

places = Blueprint('places', __name__, url_prefix='/places')


# Return all the places for a specific trip  
@places.route('/<trip_id>', methods=['GET'])
def get_places(trip_id):

    # Verify trip
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    if not trip:
        return jsonify({"message": f"No trip with id {trip_id}"}), 400
    
    # Get places for trip
    places = Place.query.filter_by(trip_id=trip_id).all()
    
    # Format places to send to frontend
    serialized_places = serialize_places(places)
    return serialized_places, 200


# Add place to list before itinerary created and add place to saved list after itinerary created
@places.route('/add/<trip_id>', methods=['POST'])
def add_place(trip_id):

    place_data = request.get_json()

    api_id = place_data['apiId']
    trip_place_id = place_data['id']      # id refers to the positional id
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

    place = Place(api_id, trip_place_id, name, address, img_url, info, favorite, 
                  category, phone_number, rating, summary, website, avg_visit_time, lat, long, in_itinerary, trip_id)

    db.session.add(place)
    db.session.commit()

    # Validate that the place has been added and return place id
    if place.place_id:
        return jsonify({"placeId": place.place_id}), 200
    else:
        return jsonify({"message": "Place could not be added"}), 500


# Deletes place
@places.route('/delete/<place_id>', methods=['DELETE'])
def delete_place(place_id):

    place = Place.query.filter_by(place_id=place_id).first()
    if not place:
        return jsonify({"message": f"No such place {place_id}"}), 400
    
    # Update database
    db.session.delete(place)
    db.session.commit()

    # Validate that the place has been deleted
    place_record = Place.query.filter_by(place_id=place_id).first()
    if not place_record:
        return jsonify({"message": "Place deleted"}), 200
    else:
        return jsonify({"message": f"Place {place_id} deletion failed"}), 500


# deletes multiple places
@places.route('/delete', methods=['DELETE'])
def delete_places():

    data = request.get_json()
    place_ids = data['placeIds']

    for place_id in place_ids:
        place = Place.query.filter_by(place_id=place_id).first()
        if not place:
            return jsonify({"message": f"No such place {place_id}"}), 400
        db.session.delete(place)
    
    db.session.commit()

    for place_id in place_ids:
        place = Place.query.filter_by(place_id=place_id).first()
        if place:
            return jsonify({"message": f"Place {place_id} not deleted"}), 500

    return jsonify({"message": "Places deleted"}), 200


# delete all places in a trip
@places.route('/delete-all/<trip_id>', methods=['DELETE'])
def delete_all_places(trip_id):

    trip = Trip.query.filter_by(trip_id=trip_id).first()
    if (not trip):
        return jsonify({"message": f"Trip {trip_id} not found"}), 404
    
    places = trip.place

    for place in places:
        db.session.delete(place)
    
    db.session.commit()

    places = Place.query.filter_by(trip_id=trip_id).all()

    if (len(places) != 0):
        return jsonify({"message": "Places not deleted"}), 500

    return jsonify({"message": "Places deleted"}), 200


# Moves place to new day
@places.route('/update/<place_id>', methods=['PATCH'])
def update_place(place_id):

    place = Place.query.filter_by(place_id=place_id).first()
    print(place)
    if not place:
        return jsonify({"message": f"No place {place_id}"}) , 400

    data = request.get_json()
    new_day_id = data['dayId']
    
    # Update place with new day_id
    place.day_id = new_day_id
    place.in_itinerary = data['inItinerary']

    # Update database
    db.session.commit()

    # Validate data has been updated
    if place.day_id == new_day_id:
        return jsonify({"message": f"Place updated to day: {new_day_id}"}) , 200
    else:
        return jsonify({"message": "Place failed to update"}), 500

# Move/Swap all places in a day to another day
@places.route('/move-days/<trip_id>', methods=['PATCH'])
def move_day_places(trip_id):

    data = request.get_json()
    src_day_id = data['sourceDayId']
    dest_day_id = data['destDayId']
    swap = data['swap']

    try:
        # Get all the places in the specified days
        src_places = Place.query.filter_by(trip_id=trip_id, day_id=src_day_id).all()
        dest_places = Place.query.filter_by(trip_id=trip_id, day_id=dest_day_id).all()

        # Move places from source day to destination day
        replace_day_id(src_places, src_day_id, dest_day_id)
        
        if(swap):
            # Move places from destination day to source day
            replace_day_id(dest_places, dest_day_id, src_day_id)

        db.session.commit()

        return jsonify({"message": "Successfully moved places"}), 200
    except Exception as e:
        return jsonify({"message": f'Failed: {e}'}), 502