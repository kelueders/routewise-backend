# EXTERNAL
from flask import Blueprint, request, redirect, url_for

# INTERNAL
from app.models import User, UserInfo, user_schema, user_info_schema, db

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Checks the code the user enters on the frontend to see if it equals the decided code
# If it's the same, then will change user has_access attribute to True
@auth.route('/check_code/', methods = ['GET', 'PATCH'])
def check_code():

    entry_code = "12445"

    uid = request.json['uid']
    passcode = request.json['passcode']

    user = User.query.filter_by(uid = uid).first()

    if passcode == entry_code:
        user.has_access = True
        db.session.commit()
        return "User now has access"
    else:
        return "Sorry, incorrect access code"

# Checks if the user has the value 'True' for their has_access attribute
@auth.route('/check_auth/<uid>', methods=['GET'])
def check_auth(uid):
    
    user = User.query.filter_by(uid = uid).first()

    if user.has_access == True:
        return redirect(url_for(''))


