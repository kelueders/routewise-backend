# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from app.models import User, UserInfo, user_schema, db

profile = Blueprint('profile', __name__, url_prefix='/profile')

# Creates a new user in the database
@profile.route('/user', methods=['POST'])
def add_user():
    uid = request.json['uid']
    username = request.json['username']
    email = request.json['email']
    has_access = False

    # Check if the user exists
    if User.query.filter_by(uid=uid).first():
        return jsonify({"message": "User has already been added to the database."}), 400

    new_user = User(uid, username, email, has_access)

    db.session.add(new_user)
    db.session.commit()

    # Send back user if correctly added to database
    user = User.query.filter_by(uid=new_user.uid).first()
    if user:
        response = user_schema.dump(user)
        print(response)
        return jsonify(response), 200
    else:
        return jsonify({"message": f'Failed adding user {uid}'}), 500

@profile.route('/test', methods=['POST', 'GET'])
def test():
    return "Waking up!", 200

# Creates a user info row attached to a specific user
@profile.route('/user_info', methods=['POST', 'GET'])
def add_user_info():

    # Get requested data for user and categories
    uid = request.json['uid']
    # Make sure user exists
    if not User.query.filter_by(uid=uid).first():
        return jsonify({"message": "User has not been created."}), 400

    categories = request.json['categories']

    shopping = categories['shopping']
    nature = categories['nature']
    landmarks = categories['landmarks']
    entertainment = categories['entertainment']
    relaxation = categories['relaxation']
    food = categories['food']
    arts = categories['arts']    

    # Create new user info
    user_info = UserInfo(uid, shopping, nature, landmarks, entertainment, relaxation, food, arts)

    db.session.add(user_info)
    db.session.commit()

    user_info_record = UserInfo.query.filter_by(user_uid=uid).first()
    if user_info_record:
        return jsonify({"message": f"Hello {user_info_record.user.username}"}), 200
    else:
        return jsonify({"message": "Failed adding user info"}), 500