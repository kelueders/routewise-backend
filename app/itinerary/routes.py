# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from app.models import Place, Trip, Day, places_schema, days_schema
from .itinerary import create_itinerary

itinerary = Blueprint('itinerary', __name__, url_prefix='/itinerary')

@itinerary.route('/createday/<trip_id>', methods=['POST', 'GET'])
def create_day(trip_id):

    if trip_id:
        places = Place.query.filter_by(trip_id = trip_id).all()
        response = places_schema.dump(places)
        jsonify(response)

        trip = Trip.query.filter_by(trip_id = trip_id).first()

        
        
        days = create_itinerary(response, trip.duration)
        # print(days)
        days = days_schema.dump(days)
        # print(days)

        # for day in days:
        #     day = Day()
        
        return jsonify(days)

    
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401