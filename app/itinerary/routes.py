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
        
        day_data = create_itinerary(response, trip.duration)

        current_date = trip.start_date

        days = day_data['days']
        day_order = day_data['day_order']

        for day_num in day_order:
            day = days[day_num]

            date_short = current_date.strftime('%m/%d')
            week_day = current_date.strftime('%a')
            date_converted = current_date.strftime('%A, %B %#d')
            day_name = ""

            new_day = Day(current_date, date_converted, date_short, week_day, day_name, trip_id)

            db.session.add(new_day)

            day["date_formatted"] = current_date
            day["date_converted"] = date_converted
            day["date_short"] = date_short
            day["day_short"] = week_day
            day_name = ""

            current_date += timedelta(1)       # increments by 1 the day that is added to the trip, starting at the trip start date

        db.session.commit()

        for day_num in day_order:
            day = days[day_num]

            new_day = Day.query.filter_by(date_formatted = day["date_formatted"]).first()

            for place_id in day['placeIds']:
                place = Place.query.filter_by(local_id = place_id, trip_id = trip_id).first()

                place.day_id = new_day.day_id
            
                db.session.commit()
                
        return jsonify(days)

    
    else:
        return jsonify({'message': 'Trip ID is missing'}), 401