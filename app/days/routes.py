# EXTERNAL
from flask import Blueprint, redirect, request, jsonify, url_for

# INTERNAL
from ..models import Trip, Place, Day, db, trips_schema
from ..global_helpers import serialize_places, add_places, create_add_days

days = Blueprint('days', __name__, url_prefix='/days')


@days.route('/update-name/<day_id>', methods=['PATCH'])
def update_day_name(day_id):
    
    day = Day.query.filter_by(day_id=day_id).first()

    data = request.get_json()
    day.name = data['dayName']

    db.session.commit()

    day = Day.query.filter_by(day_id=day_id).first()
    if day.name != data['dayName']:
        return jsonify({"message": "Day Name Not Updated"}), 500
    
    return jsonify({"message": "Day Name Updated"}), 200