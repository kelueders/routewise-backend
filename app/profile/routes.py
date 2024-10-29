# EXTERNAL
from flask import Blueprint, request, jsonify, redirect, url_for

# INTERNAL
from app.models import User, UserInfo, user_schema, user_info_schema, db

profile = Blueprint('profile', __name__, url_prefix='/profile')

# Creates a new user in the database
@profile.route('/user', methods=['POST'])
def add_user():
    uid = request.json['uid']
    email = request.json['email']
    username = ''
    first_name = ''
    last_name = ''
    has_access = False

    if User.query.filter_by(uid = uid).first():
        return jsonify({"message": "User has already been added to the database."}), 400

    data = request.get_json()
    if 'username' in data:
        username = data['username']

        # check to see if username does not exists for any user
        db_user = User.query.filter_by(username=username).first()
        if db_user and db_user.uid != uid:
            return jsonify({"message": "Username already exists"}), 400
    
    if 'firstName' in data:
        first_name = request.json['firstName']

    if 'lastName' in data:
        last_name = request.json['lastName']

    new_user = User(uid, username, email, first_name, last_name, has_access)

    db.session.add(new_user)
    db.session.commit()

    # Send back user data if correctly added to database
    if new_user.id:
        response = user_schema.dump(new_user)
        return jsonify(response), 200
    else:
        return jsonify({"message": f'Failed adding user {uid}'}), 500


# get user data
@profile.route('/user/<string:uid>', methods=['GET'])
def get_user(uid):
    
    user = User.query.filter_by(uid=uid).first()
    if user:
        response = user_schema.dump(user)
        return jsonify(response), 200
    else:
        return jsonify({"message": f"No user {uid}"}), 400


# update user data
@profile.route('/update', methods=['PATCH'])
def update_user():
    
    uid = request.json['uid']
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return jsonify({"message": f"No user {uid}"}), 400

    data = request.get_json()
    if 'username' in data:
        username = data['username']

        # check to see if username does not exists for any user
        db_user = User.query.filter_by(username=username).first()
        if db_user and db_user.uid != uid:
            return jsonify({"message": "Username already exists"}), 400
        
        user.username = username

    if 'email' in data:
        email = data['email']
        if user.email != email:
            user.email = email
    
    if 'firstName' in data:
        first_name = data['firstName']
        if user.first_name != first_name:
            user.first_name = first_name
    
    if 'lastName' in data:
        last_name = data['lastName']
        if user.last_name != last_name:
            user.last_name = last_name
    
    db.session.commit()

    response = User.query.filter_by(uid=uid).first()
    if (response.username != user.username or response.email != user.email 
        or response.first_name != user.first_name or response.last_name != user.last_name):
        return jsonify({"message": "User unsuccessfully updated"}), 500
    return jsonify({"message": "User successfully updated"}), 200


@profile.route('/test', methods=['POST', 'GET'])
def test():
    return "Waking up!"

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