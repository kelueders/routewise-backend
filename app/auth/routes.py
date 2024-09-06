# EXTERNAL
from flask import Blueprint, request, redirect, url_for, jsonify

# INTERNAL
from app.models import User, db

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Checks the code the user enters on the frontend to see if it equals the decided code
# If it's the same, then will change user has_access attribute to True
@auth.route('/check_code/', methods = ['GET', 'PATCH'])
def check_code():

    # temporarily set as the access code
    access_code = "124453"

    # get user information
    uid = request.json['uid']
    passcode = request.json['passcode']

    user = User.query.filter_by(uid=uid).first()
    if not user:
        return jsonify({"message": f'No User {uid}'}), 400
    
    # Validate access code
    if passcode == access_code:
        # Grant access to user
        user.has_access = True
        db.session.commit()
        return jsonify({"message": "Access granted"}), 200
    else:
        # Access denied to user
        return jsonify({"message": "Access NOT granted"}), 200


