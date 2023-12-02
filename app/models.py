# EXTERNAL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

# from .helpers import LatLngType

db = SQLAlchemy()    # the database is represented in the app by the database instance
ma = Marshmallow()   # the Marshmallow instance works to serialize and deserialize objects

# model and schema for the User Table in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, unique=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    user_info = db.relationship('UserInfo', back_populates = 'user')
    trip = db.relationship('Trip', back_populates = 'user')

    def __init__(self, uid, username, email):
        self.uid = uid
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User {self.username} has been added to the database." 

class UserSchema(ma.Schema):
    class Meta:
        # These fields will be posted or returned?
        fields = ['uid', 'username', 'email']

user_schema = UserSchema()



# model and schema for the UserInfo Table in the database
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shopping = db.Column(db.Boolean, default=False, nullable=False)
    nature = db.Column(db.Boolean, default=False, nullable=False)
    landmarks = db.Column(db.Boolean, default=False, nullable=False)
    entertainment = db.Column(db.Boolean, default=False, nullable=False)
    relaxation = db.Column(db.Boolean, default=False, nullable=False)
    food = db.Column(db.Boolean, default=False, nullable=False)
    arts = db.Column(db.Boolean, default=False, nullable=False)
    uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', back_populates = 'user_info')

    def __init__(self, uid, shopping, nature, landmarks, entertainment, relaxation, food, arts):                       
        self.uid = uid
        self.shopping = shopping
        self.nature = nature
        self.landmarks = landmarks
        self.entertainment = entertainment
        self.relaxation = relaxation
        self.food = food
        self.arts = arts

    def __repr__(self):
        return f'User id {self.uid} has added survey information to the database.'
    
class UserInfoSchema(ma.Schema):
    class Meta:
        fields = ['uid', 'shopping', 'nature', 'landmarks', 'entertainment', 'relaxation', 'food', 'arts']

user_info_schema = UserInfoSchema()



# Model for Trip table
class Trip(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_name = db.Column(db.String(64))
    dest_city = db.Column(db.String(64))
    dest_state = db.Column(db.String(20))
    dest_country = db.Column(db.String(20))
    dest_country_2letter = db.Column(db.String(10))
    dest_lat = db.Column(db.Float)
    dest_long = db.Column(db.Float)
    dest_img = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    duration = db.Column(db.Integer)
    uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', back_populates = 'trip')
    place = db.relationship('Place', back_populates = 'trip')
    day = db.relationship('Day', back_populates = 'trip')

    def __init__(self, trip_name, dest_city, dest_state, dest_country, dest_country_2letter, dest_lat, dest_long, dest_img, 
                 start_date, end_date, uid):
        self.trip_name = trip_name
        self.dest_city = dest_city
        self.dest_state = dest_state
        self.dest_country = dest_country
        self.dest_country_2letter = dest_country_2letter
        self.dest_lat = dest_lat
        self.dest_long = dest_long
        self.dest_img = dest_img
        self.start_date = start_date
        self.end_date = end_date
        self.uid = uid
        self.duration = self.calc_duration(start_date, end_date)

    def __repr__(self):
        return f'User id {self.uid} has added a trip to the database.'
    
    def calc_duration(self, start_date, end_date):
        # Determining duration of trip by converting string to datetime object
        start_obj = datetime.strptime(start_date, '%m/%d/%Y').date()
        end_obj = datetime.strptime(end_date, '%m/%d/%Y').date()

        # then subtract and return type INT for days
        duration = end_obj - start_obj
        duration = duration.days + 1

        return duration
    
class TripSchema(ma.Schema):
    class Meta:
        fields = ['trip_id', 'trip_name', 'dest_city', 'dest_state', 'dest_country', 'dest_country_2letter', 
                  'dest_lat', 'dest_long', 'dest_img', 'start_date', 'end_date', 'uid', 'duration']

trip_schema = TripSchema()
trips_schema = TripSchema(many = True)

# Model for the Place table
class Place(db.Model):
    place_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_name = db.Column(db.String(120))
    geoapify_placeId = db.Column(db.String)
    place_address = db.Column(db.String(120))
    place_img = db.Column(db.String)
    info = db.Column(db.String)
    favorite = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(64))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)      
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.day_id'))
    trip = db.relationship('Trip', back_populates='place')
    day = db.relationship('Day', back_populates='place')

    def __init__(self, place_name, geoapify_placeId, place_address, place_img, info, favorite, category, lat, long, trip_id):
        self.place_name = place_name
        self.geoapify_placeId = geoapify_placeId
        self.place_address = place_address
        self.place_img = place_img
        self.info = info
        self.favorite = favorite
        self.category = category
        self.lat = lat
        self.long = long
        self.trip_id = trip_id

    def __repr__(self):
        return f'{self.place_name} has been added to the user trip.'
    
class PlaceSchema(ma.Schema):
    class Meta:
        fields = ['place_id', 'place_name', 'geoapify_placeId', 'place_address', 'place_img', 'info', 
                  'favorite', 'category', 'lat', 'long', 'trip_id']

place_schema = PlaceSchema()
places_schema = PlaceSchema(many = True)

# Model for Day Table
class Day(db.Model):
    day_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(60))
    date_short = db.Column(db.String(60))
    week_day = db.Column(db.String(60))
    day_name = db.Column(db.String(60), nullable=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), nullable=False)
    trip = db.relationship('Trip', back_populates='day')
    place = db.relationship('Place', back_populates='day')

    def __init__(self, date, date_short, week_day, day_name, trip_id):
        self.date = date
        self.date_short = date_short
        self.week_day = week_day
        self.day_name = day_name
        self.trip_id = trip_id
    
    def __repr__(self):
        return f'{self.date} has added a trip to the database.'
    
class DaySchema(ma.Schema):
    class Meta:
        fields = ['day_id', 'date', 'date_short', 'week_day', 'day_name', 'trip_id']

day_schema = DaySchema()
days_schema = DaySchema(many = True)
    

