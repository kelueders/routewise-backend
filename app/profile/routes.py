# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from .models import User, UserInfo, user_schema, user_info_schema, db

profile = Blueprint('profile', __name__, url_prefix='/profile')

# Creates a new user in the database
@profile.route('/user', methods=['POST'])
def add_user():
    id = request.json['uid']
    username = request.json['displayName']
    email = request.json['email']

    new_user = User(id, username, email)

    return f'It worked. ID: {new_user.id} Username: {new_user.username} Email: {new_user.email}'

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)

# Creates a user info row attached to a specific user
@profile.route('/user_info', methods=['POST'])
def add_userinfo():
    # id = request.json['id']                 # does this need to be here if it is being autoincremented when it is instantiated?
    shopping = request.json['shopping']
    nature = request.json['nature']
    landmarks = request.json['landmarks']
    entertainment = request.json['entertainment']
    relaxation = request.json['relaxation']
    food = request.json['food']
    arts = request.json['arts']
    user_id = request.json['user_id']          # how does this connect up with the correct user???

    new_userinfo = UserInfo(shopping, nature, landmarks, entertainment, relaxation, food, arts, user_id)

    db.session.add(new_userinfo)
    db.session.commit()

    user_info = UserInfo.query.get(new_userinfo.id)

    return user_info_schema.jsonify(user_info)