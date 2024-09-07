# EXTERNAL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()    # the database is represented in the app by the database instance
ma = Marshmallow()   # the Marshmallow instance works to serialize and deserialize objects

# model and schema for the User Table in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, unique=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    has_access = db.Column(db.Boolean, default=False, nullable=True)
    user_info = db.relationship('UserInfo', back_populates='user')
    trip = db.relationship('Trip', back_populates='user')

    def __init__(self, uid, username, email, has_access):
        self.uid = uid
        self.username = username
        self.email = email
        self.has_access = has_access

    def __repr__(self):
        return f"User {self.username} has been added to the database." 

class UserSchema(ma.Schema):
    class Meta:
        # These fields will be posted or returned?
        fields = ['uid', 'username', 'email', 'hasAccess']

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
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', back_populates='user_info')

    def __init__(self, user_uid, shopping, nature, landmarks, entertainment, relaxation, food, arts):                       
        self.user_uid = user_uid
        self.shopping = shopping
        self.nature = nature
        self.landmarks = landmarks
        self.entertainment = entertainment
        self.relaxation = relaxation
        self.food = food
        self.arts = arts

    def __repr__(self):
        return f'{self.user_uid} User Object'
    
class UserInfoSchema(ma.Schema):
    class Meta:
        fields = ['userUid', 'shopping', 'nature', 'landmarks', 'entertainment', 'relaxation', 'food', 'arts']

user_info_schema = UserInfoSchema()



# Model for Trip table
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    dest_city = db.Column(db.String)
    dest_state = db.Column(db.String(255))
    dest_country = db.Column(db.String)
    dest_country_abbr = db.Column(db.String(10))
    dest_lat = db.Column(db.Float)
    dest_long = db.Column(db.Float)
    dest_img_url = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_itinerary = db.Column(db.Boolean, default=False, nullable=True)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', back_populates='trip')
    place = db.relationship('Place', back_populates='trip')
    day = db.relationship('Day', back_populates='trip')

    def __init__(self, name, dest_city, dest_state, dest_country, dest_country_abbr, dest_lat, dest_long, 
                 dest_img_url, start_date, end_date, user_uid):
        self.name = name
        self.dest_city = dest_city
        self.dest_state = dest_state
        self.dest_country = dest_country
        self.dest_country_abbr = dest_country_abbr
        self.dest_lat = dest_lat
        self.dest_long = dest_long
        self.dest_img_url = dest_img_url
        self.start_date = start_date
        self.end_date = end_date
        self.user_uid = user_uid
        self.duration = self.calc_duration(start_date, end_date)

    def __repr__(self):
        return f'{self.id} Trip Object'
    
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
        fields = ['id', 'name', 'destCity', 'destState', 'destCountry', 'destCountryAbbr', 
                  'destLat', 'destLong', 'destImgUrl', 'startDate', 'endDate', 'isItinerary', 
                  'userUid', 'duration']

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)



# Model for the Place table
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.String)
    position_id = db.Column(db.Integer)    # int - index of that place within the trip (to account for a person adding the same location twice in a trip)
    name = db.Column(db.String)
    address = db.Column(db.String)
    img_url = db.Column(db.String)
    info = db.Column(db.String)
    favorite = db.Column(db.Boolean, default=False)
    category = db.Column(db.String, default=None, nullable=True)
    phone_number = db.Column(db.String, default=None, nullable=True)
    rating = db.Column(db.String, default=None, nullable=True)
    summary = db.Column(db.String, default=None, nullable=True)
    website = db.Column(db.String, default=None, nullable=True)
    avg_visit_time = db.Column(db.Float, default=60, nullable=True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    in_itinerary = db.Column(db.Boolean, default=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    trip = db.relationship('Trip', back_populates='place')
    day = db.relationship('Day', back_populates='place')

    def __init__(self, api_id, position_id, name, address, img_url, info, favorite, category, 
                 phone_number, rating, summary, website, avg_visit_time, lat, long, in_itinerary, 
                 trip_id):
        self.api_id = api_id
        self.position_id = position_id
        self.name = name
        self.address = address
        self.img_url = img_url
        self.info = info
        self.favorite = favorite
        self.category = category
        self.phone_number = phone_number
        self.rating = rating
        self.summary = summary
        self.website = website
        self.avg_visit_time = avg_visit_time
        self.lat = lat
        self.long = long
        self.in_itinerary = in_itinerary
        self.trip_id = trip_id

    def update_day_id(self, day_id):
        self.day_id = day_id

    def __repr__(self):
        return f'{self.name} Place Object'
    
class PlaceSchema(ma.Schema):
    class Meta:
        fields = ['apiId', 'positionId', 'name', 'address', 'imgUrl', 'info', 'favorite', 
                  'category', 'phoneNumber', 'rating', 'summary', 'website', 'avgVisitTime', 
                  'lat', 'long', 'inItinerary', 'tripId', 'dayId']

place_schema = PlaceSchema()
places_schema = PlaceSchema(many=True)



# Model for Day Table
class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=True)
    date_formatted = db.Column(db.Date)
    date_converted = db.Column(db.String(60))
    date_short = db.Column(db.String(60))
    week_day = db.Column(db.String(60))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='day')
    place = db.relationship('Place', back_populates='day')

    def __init__(self, name, date_formatted, date_converted, date_short, week_day, trip_id):
        self.name = name
        self.date_formatted = date_formatted
        self.date_converted = date_converted
        self.date_short = date_short
        self.week_day = week_day
        self.trip_id = trip_id
    
    def __repr__(self):
        return f'{self.date_formatted} Day Object.'
    
class DaySchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'dateFormatted', 'dateConverted', 'dateShort', 'weekDay', 'tripId']

day_schema = DaySchema()
days_schema = DaySchema(many=True)
