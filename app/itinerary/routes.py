# EXTERNAL
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

# INTERNAL
from app.models import Place, Trip, Day, places_schema, days_schema, db
from .itinerary import create_itinerary

itinerary = Blueprint('itinerary', __name__, url_prefix='/itinerary')

@itinerary.route('/createdays/<trip_id>', methods=['POST', 'GET'])
def create_days(trip_id):

    if trip_id:
        places = Place.query.filter_by(trip_id = trip_id).all()
        response = places_schema.dump(places)
        jsonify(response)

        trip = Trip.query.filter_by(trip_id = trip_id).first()
        
        days = create_itinerary(response, trip.duration)
        print(days)
        days = days_schema.dump(days)                 # do we need this?
        print(days)

        current_date = trip.start_date

        for day in days:

            date_short = current_date.strftime('%m/%d')
            week_day = current_date.strftime('%a')
            day_name = ""

            day = Day(current_date, date_short, week_day, day_name, trip_id)

            # db.session.add(day)

            current_date += timedelta(1)

        db.session.commit()


        day_id = Day.query.filter_by(date = current_date).first()

        
        return jsonify(days)

    
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401