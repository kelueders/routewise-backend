# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from ..models import Day, db

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