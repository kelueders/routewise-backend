# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from app.models import User, UserInfo, user_schema, user_info_schema, db

profile = Blueprint('profile', __name__, url_prefix='/profile')

# Creates a new user in the database
@profile.route('/user', methods=['POST'])
def add_user():
    uid = request.json['uid']
    username = request.json['displayName']
    email = request.json['email']

    new_user = User(uid, username, email)

    db.session.add(new_user)
    db.session.commit()

    # user = User.query.get(new_user.uid)

    # will send back the row with name, email, and uid that matches this uid
    user = User.query.filter_by(uid=new_user.uid).first()

    return user_schema.jsonify(user)

    # return f'It worked. ID: {new_user.uid} Username: {new_user.username} Email: {new_user.email}'

@profile.route('/test', methods=['POST', 'GET'])
def test():
    return "It's working!"

# Creates a user info row attached to a specific user
@profile.route('/user_info', methods=['POST', 'GET'])
def add_userinfo():

    uid = request.json['uid']
    categories = request.json['categories']      # this returns a dictionary

    shopping = categories['shopping']
    nature = categories['nature']
    landmarks = categories['landmarks']
    entertainment = categories['entertainment']
    relaxation = categories['relaxation']
    food = categories['food']
    arts = categories['arts']    

    new_userinfo = UserInfo(uid, shopping, nature, landmarks, entertainment, relaxation, food, arts)

    db.session.add(new_userinfo)
    db.session.commit()

    # user_info = UserInfo.query.get(new_userinfo.id)

    # return user_info_schema.jsonify(user_info)

    return 'hello'