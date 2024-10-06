# EXTERNAL
from flask import Blueprint, request, jsonify

# INTERNAL
from app.models import User, UserInfo, user_schema, db, user_info_schema

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
    if new_user.id:
        response = user_schema.dump(new_user)
        return jsonify(response), 200
    else:
        return jsonify({"message": f'Failed adding user {uid}'}), 500


@profile.route('/test', methods=['POST', 'GET'])
def test():
    return "Waking up!", 200


# Creates a user info row attached to a specific user
@profile.route('/user-info', methods=['POST', 'GET'])
def add_user_info():

    uid = request.json['uid']
    # Make sure user exists
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return jsonify({"message": "User has not been created."}), 400

    if request.method == 'GET':
        user_info = user.user_info[0]
        if user_info:
            schema = user_info_schema.dump(user_info)
            return jsonify(schema), 200
        else:
            return jsonify({"message": f'There is no user info for user: {uid}'}), 400
        
    elif request.method == 'POST':
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

        if user_info.id:
            return jsonify({"message": f"Hello {user_info.user.username}"}), 200
        else:
            return jsonify({"message": "Failed adding user info"}), 500