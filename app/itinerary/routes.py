# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from ..models import Place, Trip, db
from ..global_helpers import serialize_places, replace_day_id, create_add_days
from .itinerary import Itinerary

itinerary = Blueprint('itinerary', __name__, url_prefix='/itinerary')


# Create itinerary with places sorted into days
@itinerary.route('/generate/<trip_id>', methods=['PATCH'])
def generate_itinerary(trip_id):
    
    # Check that there is a trip with the id
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    if not trip:
        return jsonify({'message': 'No Trip for trip ID'}), 404
    
    places = trip.place

    # Create days if they havent been created already
    days_data = trip.day
    days = {}
    if days_data:
        # serialize days
        for i, day_data in enumerate(days_data):
            day_dict = day_data.serialize(num=i+1, empty=True)
            days[day_dict['id']] = day_dict
    else:
        days = create_add_days(trip)

    # Create Itinerary data
    itinerary = Itinerary(trip_id, places)
    itinerary_data = itinerary.generate()   # multi-dimen array - rows=days, cols=place_ids

    # Populate saved_places and days with places from itinerary_data
    saved_places_ids = []
    for i, day_row in enumerate(itinerary_data):
        for j, trip_place_id in enumerate(day_row):
            # Get place
            place = next((p for p in places if p.trip_place_id == trip_place_id), None)

            days_day_id = f'day-{i + 1}'
            if days_day_id in days:
                # Place is in an existing day
                # Add place_id to days
                day = days[days_day_id]
                day['placeIds'].append(trip_place_id)

                # Add day_id to place, and set in_itinerary true
                place.day_id = day['dayId']
                place.in_itinerary = True
            else:
                # Place is not in an existing day
                # Set day_id to None, and in_itinerary to false
                place.day_id = None
                place.in_itinerary = False

                # Add place_id to saved places
                saved_places_ids.append(trip_place_id)

    # Update the trip 'is_itinerary' key to 'True'
    trip.is_itinerary = True
    db.session.commit()

    # Serializes the list of places (see global_helpers.py)
    serialized_places = serialize_places(places)
    
    # Packages the data in order to be rendered on the frontend
    return {
        "tripId": int(trip_id),
        "lastPlaceId": places[-1].trip_place_id,
        "places": serialized_places,
        "days": days,
        "dayOrder": list(days.keys()),
        "savedPlaces": { 
            "placeIds": saved_places_ids,
            "addresses": list(map(lambda x: serialized_places[x]["address"], saved_places_ids))
        }
    }, 200


# Add a place to a specific day in the trip when there is already an itinerary created    
@itinerary.route('/add-one-place/<trip_id>', methods=['POST'])
def add_one_place(trip_id):

    data = request.get_json()
    place_data = data['place']

    trip_place_id = place_data['id']      # id refers to the positional id
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

    # Add in day id if place is assigned a day in itinerary
    if data['dayId']:
        day_id = data['dayId']
        in_itinerary = True
    else:
        day_id = None
        in_itinerary = False
    
    # Create new place
    place = Place(api_Id, trip_place_id, name, address, img_url, info, favorite, category, phone_number, 
                  rating, summary, website, avg_visit_time, lat, long, in_itinerary, trip_id)
    place.update_day_id(day_id)
    
    # Add new place to database
    db.session.add(place)
    db.session.commit()

    # RETURN THE place id to the front end if successfully added to database
    if place.place_id:
        return jsonify({"placeId": place.place_id}), 200
    else:
        return jsonify({"message": "Place could not be added"}), 500
