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
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    has_access = db.Column(db.Boolean, default=False, nullable=True)
    user_info = db.relationship('UserInfo', back_populates='user')
    trip = db.relationship('Trip', back_populates='user')

    def __init__(self, uid, username, email, first_name, last_name, has_access):
        self.uid = uid
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.has_access = has_access

    def __repr__(self):
        return f"User {self.username} has been added to the database." 

class UserSchema(ma.Schema):
    firstName = ma.String(attribute='first_name')
    lastName = ma.String(attribute='last_name')
    hasAccess = ma.Boolean(attribute='has_access')

    class Meta:
        # These fields will be posted or returned?
        fields = ['uid', 'username', 'email', 'firstName', 'lastName', 'hasAccess']

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
    user = db.relationship('User', back_populates='user_info')

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
        return f'{self.uid} User Object'
    
class UserInfoSchema(ma.Schema):

    class Meta:
        fields = ['uid', 'shopping', 'nature', 'landmarks', 'entertainment', 'relaxation', 'food', 'arts']

user_info_schema = UserInfoSchema()



# Model for Trip table
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String(255))
    country = db.Column(db.String)
    country_abbr = db.Column(db.String(10))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    img_url = db.Column(db.String)
    start_date = db.Column(db.String)       # mm/dd/yyyy
    end_date = db.Column(db.String)         # mm/dd/yyyy
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_itinerary = db.Column(db.Boolean, default=False, nullable=True)
    uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', back_populates='trip')
    place = db.relationship('Place', back_populates='trip')
    day = db.relationship('Day', back_populates='trip')

    date_format = '%m/%d/%Y'

    def __init__(self, name, city, state, country, country_abbr, lat, long, img_url, 
                 start_date, end_date, uid):
        self.name = name
        self.city = city
        self.state = state
        self.country = country
        self.country_abbr = country_abbr
        self.lat = lat
        self.long = long
        self.img_url = img_url
        self.start_date = start_date                # mm/dd/yyyy
        self.end_date = end_date                    # mm/dd/yyyy
        self.uid = uid
        self.duration = self.calc_duration()

    def __repr__(self):
        return f'{self.id} Trip Object'
    
    def calc_duration(self):
        # Determining duration of trip by converting string to datetime object
        start_obj = datetime.strptime(self.start_date, self.date_format).date()
        end_obj = datetime.strptime(self.end_date, self.date_format).date()

        # then subtract and return type INT for days
        duration = end_obj - start_obj
        duration = duration.days + 1

        return duration
    
    def convert_to_datetime(self, date):
        return datetime.strptime(date, self.date_format).date()
    
class TripSchema(ma.Schema):
    countryAbbr = ma.String(attribute='country_abbr')
    imgUrl = ma.String(attribute='img_url')
    startDate = ma.String(attribute='start_date')
    endDate = ma.String(attribute='end_date')
    isItinerary = ma.Boolean(attribute='is_itinerary')

    class Meta:
        fields = ['id', 'name', 'city', 'state', 'country', 'countryAbbr', 'lat', 'long', 'imgUrl', 
                  'startDate', 'endDate', 'isItinerary', 'uid', 'duration']

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
    day_id = db.Column(db.Integer, db.ForeignKey('day.day_id'))
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
    placeId = ma.Integer(attribute='id')
    apiId = ma.String(attribute='api_id')
    positionId = ma.Integer(attribute='position_id')
    imgUrl = ma.String(attribute='img_url')
    phoneNumber = ma.String(attribute='phone_number')
    avgVisitTime = ma.Float(attribute='avg_visit_time')
    inItinerary = ma.Boolean(attribute='in_itinerary')
    tripId = ma.Integer(attribute='trip_id')
    dayId = ma.Integer(attribute='day_id')

    class Meta:
        fields = ['placeId', 'apiId', 'positionId', 'name', 'address', 'imgUrl', 'info', 'favorite', 
                  'category', 'phoneNumber', 'rating', 'summary', 'website', 'avgVisitTime', 
                  'lat', 'long', 'inItinerary', 'tripId', 'dayId']

place_schema = PlaceSchema()
places_schema = PlaceSchema(many=True)



# Model for Day Table
class Day(db.Model):
    day_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_num = db.Column(db.String)                      # day-#
    name = db.Column(db.String(60), nullable=True)      # optional name for day
    date_mm_dd_yyyy = db.Column(db.String)              # mm/dd/yyyy
    date_weekday_month_day = db.Column(db.String(60))   # Weekday, Month day
    date_mm_dd = db.Column(db.String(60))               # mm/dd
    weekday = db.Column(db.String(60))                  # Weekday abbreviation
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='day')
    place = db.relationship('Place', back_populates='day')

    def __init__(self, num, name, date, trip_id):
        self.add_day_num(num)
        self.name = name
        self.date_mm_dd_yyyy = date.strftime('%m/%d/%Y')            # mm/dd/yyyy
        self.date_weekday_month_day = date.strftime('%A, %B %#d')   # Weekday, Month day
        self.date_mm_dd = date.strftime('%m/%d')                    # mm/dd
        self.weekday = date.strftime('%a')                          # Weekday abbreviation
        self.trip_id = trip_id
    
    def __repr__(self):
        return f'{self.date_mm_dd_yyyy} Day Object.'
    
    def add_day_num(self, num):
        self.day_num = f'day-{num}'

    def serialize(self, num, empty):
        if not self.day_num:
            self.add_day_num(num)
        
        day_dict = day_schema.dump(self)

        if empty:
            day_dict['placeIds'] = []
        else:
            day_dict['placeIds'] = [ place.positionId for place in self.place ]
        
        return day_dict
    
class DaySchema(ma.Schema):
    dayId = ma.Integer(attribute='day_id')
    id = ma.String(attribute='day_num')
    dateMMDDYYYY = ma.String(attribute='date_mm_dd_yyyy')
    dateWeekdayMonthDay = ma.String(attribute='date_weekday_month_day')
    dateMMDD = ma.String(attribute='date_mm_dd')

    class Meta:
        fields = ['dayId', 'id', 'name', 'dateMMDDYYYY', 'dateWeekdayMonthDay', 'dateMMDD', 'weekday']

day_schema = DaySchema()
days_schema = DaySchema(many=True)
