# EXTERNAL
from flask import Blueprint, request, jsonify
from datetime import timedelta

# INTERNAL
from ..models import Place, Trip, Day, db
from ..global_helpers import create_day_dict, serialize_places, replace_day_id
from .itinerary import Itinerary

itinerary = Blueprint('itinerary', __name__, url_prefix='/itinerary')

# Create itinerary with places sorted into days
@itinerary.route('/generate/<trip_id>', methods=['GET', 'PATCH'])
def generate_itinerary(trip_id):
    
    # Check that there is a trip with the id
    trip = Trip.query.filter_by(id=trip_id).first()
    if not trip:
        return jsonify({'message': 'No Trip for trip ID'}), 404
    
    places = Place.query.filter_by(trip_id=trip_id).all()

    # Create days if they havent been created already
    days_data = Day.query.filter_by(trip_id=trip_id).all()
    days = {}
    if days_data:
        # serialize days
        for i, day_data in enumerate(days_data):
            day_dict = create_day_dict(i + 1, day_data)
            days[day_dict['dayNum']] = day_dict
    else:
        current_date = trip.convert_to_datetime(trip.start_date)
        for i in range(1, trip.duration + 1):
            # Create and add day to database
            new_day = Day(i, '', current_date, trip_id)

            # Serialize day
            day_dict = create_day_dict(i, new_day)
            days[day_dict['dayNum']] = day_dict

            db.session.add(new_day)

            # Update day with id created from database
            new_day = Day.query.filter_by(day_num=day_dict['dayNum'], trip_id=trip_id).first()
            days[day_dict['dayNum']]['id'] = new_day.id

            # Increments by 1 the day that is added to the trip, starting at the trip start date
            current_date += timedelta(1)

    # Create Itinerary data
    itinerary = Itinerary(trip_id)
    itinerary_data = itinerary.generate()       # multi-dimen array - rows=days, cols=place_ids

    # Populate saved_places and days with places from itinerary_data
    saved_places_ids = []
    for i, day_row in enumerate(itinerary_data):
        for j, place_position_id in enumerate(day_row):
            # Get place
            place = Place.query.filter_by(position_id=place_position_id, trip_id=trip_id).first()

            days_day_id = f'day-{i + 1}'
            if days_day_id in days:
                # Place is in an existing day
                # Add place_id to days
                day = days[days_day_id]
                day['placeIds'].append(place_position_id)

                # Add day_id to place, and set in_itinerary true
                place.day_id = day['id']
                place.in_itinerary = True    
            else:
                # Place is not in an existing day
                # Set day_id to None, and in_itinerary to false
                place.day_id = None
                place.in_itinerary = False

                # Add place_id to saved places
                saved_places_ids.append(place_position_id)

    # Update the trip 'is_itinerary' key to 'True'
    trip.is_itinerary = True
    db.session.commit()

    # Serializes the list of places (see global_helpers.py)
    serialized_places = serialize_places(Place.query.filter_by(trip_id=trip_id).all())
    # Remove position_id to coordinate with the front end
    for place_position_id in serialized_places:
        serialized_places[place_position_id]['id'] = serialized_places[place_position_id].pop('positionId') 
    
    # Packages the data in order to be rendered on the frontend
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


# Add a place to a specific day in the trip when there is already an itinerary created    
@itinerary.route('/add-one-place/<trip_id>', methods=['POST', 'GET'])
def add_one_place(trip_id):
    # Get data from request
    data = request.get_json()
    place_data = data['place']
    position_id = place_data['positionId']
    api_Id = place_data['apiId']
    name = place_data['name']
    address = place_data['address']
    img_url = place_data['imgUrl']
    favorite = place_data['favorite']
    category = place_data.get('category', None)
    phone_number = place_data.get('phoneNumber', None)
    rating = place_data.get('rating', None)
    summary = place_data.get('summary', None)
    website = place_data.get('website', None)
    avg_visit_time = place_data.get('avgVisitTime', 60)
    info = place_data['info']
    lat = place_data['lat']
    long = place_data['long']

    # Add in day_id if place is assigned a day in itinerary
    if data['dayId']:
        day_id = data['dayId']
        in_itinerary = True
    else:
        day_id = None
        in_itinerary = False
    
    # Create new place
    place = Place(api_Id, position_id, name, address, img_url, info, 
                  favorite, category, phone_number, rating, summary, website, avg_visit_time, 
                  lat, long, in_itinerary, trip_id)
    place.update_day_id(day_id)
    
    # Add new place to database
    db.session.add(place)
    db.session.commit()

    # RETURN THE place_id to the front end if successfully added to database
    place_record = Place.query.filter_by(position_id=position_id, trip_id=trip_id).first()
    if place_record:
        return str(place_record.id), 200
    else:
        return jsonify({"message": "Place could not be added"}), 500


# Deletes place
@itinerary.route('/delete-place/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    # Get place
    place = Place.query.filter_by(id=place_id).first()
    if not place:
        return jsonify({"message": f"No such place {place_id}"}), 400
    
    # Update database
    db.session.delete(place)
    db.session.commit()

    # Validate that the place has been deleted
    place_record = Place.query.filter_by(id=place_id).first()
    if not place_record:
        return jsonify({"message": "Place deleted"}), 200
    else:
        return jsonify({"message": f"Place {place_id} deletion failed"}), 500


# Moves place to new day
@itinerary.route('/update-place/<place_id>', methods=['PATCH'])
def update_place(place_id):
    # Get requested data
    data = request.get_json()
    new_day_id = data['dayId']
    place = Place.query.filter_by(id=place_id).first()
    if not place:
        return jsonify({"message": f"No place {place_id}"}) , 400

    # Update place with new day_id
    place.day_id = new_day_id
    place.in_itinerary = data['inItinerary']

    # Update database
    db.session.commit()

    # Validate data has been updated
    place_record = Place.query.filter_by(id=place_id).first()
    if place_record.day_id == new_day_id:
        return jsonify({"message": f"Place updated to day: {new_day_id}"}) , 200
    else:
        return jsonify({"message": "Place failed to update"}), 500


# Move/Swap all places in a day to another day
@itinerary.route('/move-day-places/<trip_id>', methods=['PATCH'])
def move_day_places(trip_id):
    # Get requested data
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
