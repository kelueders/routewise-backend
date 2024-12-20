# RouteWise Backend
The backend includes the api endpoints for the frontend to access the database and includes the algorithm for creating an itinerary. The project is built using the Flask framework in Python. The backend is hosted on Render. For data management, the project uses PostgreSQL.

### Tech Stack
- Python
- Flask Framework
- Gunicorn for production deployment
- PostgreSQL
- AWS RDS for PostrgreSQL
- Render (Python version: 3.11.9)
- Docker
- GitHub Actions
- Pytest for unit testing

## How to Run and Test
### Run in a development environment
1. Install the dependencies. **Note**: you may need to comment out some depenencies and manually install it.

    ``` 
    pip install -r requirements.txt 
    ```

2. Set config variables for the flask app as environment variables. Create `.env` file in the root directory and fill with the following data. Replace '****' with the secret.
    ```
    FLASK_APP = app:create_app()
    FLASK_ENV = development
    FLASK_DEBUG = true
    SECRET_KEY = '****'
    SQLALCHEMY_DATABASE_URI = ****
    PASSCODE = '****'
    ```

3. Run the program. This will launch the test environment on port 5000.

    ``` 
    flask run 
    ```

### Run in docker container
Running the program in a docker container ensures it runs in a clean enviornment. Additionally, you won't need to install the required libraries on your local machine. The environment is specified in dockerfile.

1. Install docker on your machine following the instructions on [docker](https://www.docker.com/)

2. Navigate to the directory with the dockerfile. Build the image with the tag flask-run. Make sure docker is running in the background.

    ```
    docker build -t flask-run .
    ```

3. Run the image with the -d tag to have the container running in the background and -p localhost:8000 to connect with the port. This will allow users to access the routes using port 8000.

    ```
    docker run -dp 127.0.0.1:8000:5000 flask-run
    ```

4. View if the container is active and running

    ```
    docker ps
    ```

5. To access the workspace inside the container, exec into the container using a shell space.

    ```
    docker exec -it container_id sh
    ```

4. Stop a running docker container, replace container_id with the actual ID that can be found by running the `docker ps` command.

    ```
    docker stop container_id
    ```

### Test with unit tests
There are several unit tests created for the api endpoints.

1. Update python libraries

    ```
    pip install -r requirements.txt
    ```

2. In the root directory, run the python tests
    ```
    pytest
    ```

    Running certain tests
    ```
    pytest <directory>
    ```

### Run in production
Gunicorn is used for running in a production environment. **Note: gunicorn can not run on Windows, in this case use a docker container.

1. Run the following command in a non-windows enviornment or docker container:
    ```
    gunicorn --bind 0.0.0.0:5000 wsgi:app 
    ```

## Code Structure
- / : outlines the necessary requirements to run the program
- wsgi.py : deploy flask in production environment with gunicorn
- config.py : contains environment variables needed to run app
- /.github/workflows : contains the workflows that are run through GitHub Actions
- /app : The Flask code is contained in the app directory. It also initiates the webpage for port 5000.
    - __ init__.py : contains the app for deploying the app
    - models.py : contains the schema for database models.
    - global_helpers.py : contains helper functions used in multiple files.
    - /auth : contains the api route to handle granting access to a user
    - /days : contains the api routes to handle manipulating day data from the database.
    - /itinerary : contains the algorithm to create an itinerary and the api routes to manipulate an itinerary.
    - /places : contains the api routes to handle getting and manipulating places data from the database.
    - /profile : contains the api route to handle getting and manipulating user data in the database.
    - /trip : contains the api routes to handle getting and manipulating trip data from the database.
- /tests : Contains the unit tests
    - mock_data.py : contains mock data to be used in the tests
    - config.py : runs the program testing mode on a local sqlite database
    - /auth : contains the tests for the auth api routes
    - /days : contains the tests for the days api routes
    - /itinerary : contains the tests for the itinerary api routes
    - /places : contains the tests for the places api routes
    - /profile : contains the tests for the profile api routes
    - /trip : contains the tests for the trip api routes

## API Documentation

### `GET|PATCH /auth/check-code`
- **Description**: Verify user access.
- **Request Body**: Post: update database; GET: check status.
    ```json
    {
        "uid": "",
        "passcode": ""
    }
    ```
- **Response**:
    - Status code 400, if user does not exist.
    - Status code 200, user is granted access.
    - Status code 401, user is not granted access.

### `PATCH /days/update-name/<day_id>`
- **Description**: Update day name (user created title for a trip day).
- **Request Body**:
    ```json
    {
        "dayName": ""
    }
    ```
- **Response**: Status code 200, if successful.

### `PATCH /itinerary/generate/<trip_id>`
- **Description**: Create itinerary for places and creates corresponding days.
- **Response**:
    - Status code 401, if trip does not exist.
    - Status code 200, on success.
    ```json
    {
        "dayOrder": [
            "day-1",
            ...
        ],
        "days": {
            "day-1": {
                "dateMMDD": "mm/dd",
                "dateWeekdayMonthDay": "Weekday, Month Day",
                "dateMMDDYYYY": "mm/dd/yyyy",
                "id": "day-1",
                "databaseId": 1,
                "name": "",
                "placeIds": [
                    (Integer),
                    ...
                ],
                "weekday": "Weekday Abbreviation",
            },
            ...
        },
        "places": {
            "1": {
                "address": "",
                "apiId": "",
                "avgVisitTime": (Float),
                "category": "",
                "dayDatabaseId": (Integer),
                "favorite": (Boolean),
                "geocode": [ (Float), (Float) ],
                "databaseId": (Integer, unique identifier for the element in the database),
                "imgUrl": "",
                "inItinerary": (Boolean),
                "info": "",
                "lat": (Float),
                "long": (Float),
                "phoneNumber": "",
                "id": 1 (index of place relative to a trip),
                "name": "",
                "rating": "",
                "summary": "",
                "tripId": (Integer),
                "website": ""
            },
            ...
        },
        "lastPlaceId": (Integer),
        "savedPlaces": {
            "addresses": [ "", ... ],
            "placeIds": [ (Integer), ... ]
        },
        "tripId": (Integer)
    }
    ```

### `POST /itinerary/add-one-place/<trip_id>`
- **Description**: Adds new place if itinerary hasn't been created.
- **Request Body**:
    ```json
    {
        "dayId": null/(Integer),
        "place":{
            "id": (Integer, position id),
            "apiId": "",
            "name": "",
            "info": "",
            "summary": "",
            "address": "",
            "phoneNumber": "",
            "website": "",
            "imgUrl": "",
            "category": "",
            "favorite": (Boolean),
            "lat": (Float),
            "long": (Float),
            "geocode": [ (Float), (Float) ],
            "rating": "",
            "avgVisitTime": (Float)
        }
    }
    ```
- **Response**: Status code 200 on success.
    ```json
    {
        "databaseId": (Integer)
    }
    ```

### `GET /places/<trip_id>`
- **Description**: Gets places in trip.
- **Response**:
    - Status code 400, if the trip doesn't exist.
    - Status code 200, if there are places for the trip.
    ```json
    {
        "1": {
            "address": "",
            "apiId": "",
            "avgVisitTime": (Float),
            "category": "",
            "dayDatabaseId": (Integer),
            "favorite": (Boolean),
            "geocode": [ (Float), (Float) ],
            "databaseId": (Integer, unique identifier for the element in the database),
            "imgUrl": "",
            "inItinerary": (Boolean),
            "info": "",
            "lat": (Float),
            "long": (Float),
            "phoneNumber": "",
            "id": 1 (index of place relative to a trip),
            "name": "",
            "rating": "",
            "summary": "",
            "tripId": (Integer),
            "website": ""
        },
        ...
    }
    ```

### `POST /places/add/<trip_id>`
- **Description**: Add a place to empty itinerary.
- **Request Body**:
    ```json
    {
        "apiId": "",
        "id": (Integer, positional id),
        "name": "",
        "address": "",
        "imgUrl": "",
        "info": "",
        "favorite": (Boolean),
        "category": "",
        "phoneNumber": "",
        "rating": "",
        "summary": "",
        "website": "",
        "avgVisitTime": (Float),
        "lat": (Float),
        "long": (Float)
    }
    ```
- **Response**: Status code 200 upon success.
    ```json
    {
        "databaseId": (Integer)
    }
    ```

### `DELETE /places/delete/<place_id>`
- **Description**: Deletes place from database.
- **Response**: 
    - Status code 400, if no place is found.
    - Status code 200, if place is successfully deleted.

### `DELETE /places/delete`
- **Description**: Deletes multiple places.
- **Request Body**:
    ```json
    {
        "placeIds": [ (Integer), ... ]
    }
    ```
- **Response**: Status code 200 if successful

### `DELETE /places/delete-all/<trip_id>`
- **Description**: Deletes all places related to a specified trip.
- **Response**: Status code 200 if successful

### `PATCH /places/update/<place_id>`
- **Description**: Move place to day.
- **Request Body**:
    ```json
    {
        "dayId": (Integer),
        "inItinerary": (Boolean)
    }
    ```
- **Response**:
    - Status code 400, if place doesn’t exist.
    - Status code 200, if place successfully moved.

### `PATCH /places/move-days/<trip_id>`
- **Description**: Moves/swaps all places in a day to a destination day.
- **Request Body**:
    ```json
    {
        "sourceDayId": (Integer),
        "destDayId" : (Integer),
        "swap": (Boolean)
    }
    ```
- **Response**: Status code 200, if places are successfully moved.

### `POST /trip/add`
- **Description**: Adds a new trip with optional places.
- **Request Body**:

    Empty trip
    ```json
    {
        "uid": "",
        "trip": {
            "name": "",
            "city": "",
            "state": "",
            "country": "",
            "countryAbbr": "",
            "lat": (Float),
            "long": (Float),
            "imgUrl": "",
            "startDate": "mm/dd/yyyy",
            "endDate": "mm/dd/yyyy"
        }
    }
    ```
    Trip with places
    ```json
    {
        "uid": "",
        "trip": {
            "name": "",
            "city": "",
            "state": "",
            "country": "",
            "countryAbbr": "",
            "geocode": [ (Float), (Float) ],
            "imgUrl": "",
            "startDate": "mm/dd/yyyy",
            "endDate": "mm/dd/yyyy",
            "places": [
                {
                    "id": 1,
                    "name": "",
                    "apiId": "",
                    "address": "",
                    "imgUrl": "",
                    "category": "",
                    "favorite": (Boolean),
                    "phoneNumber": "",
                    "rating": "",
                    "summary": "",
                    "website": "",
                    "info": "",
                    "lat": (Float),
                    "long": (Float)
                },
                ...
            ]
        }
    }
    ```
- **Response**: Status code 200 on success.
    ```json
    {
        "tripId": (Integer),
        "startDate": "mm/dd/yyyy",
        "endDate": "mm/dd/yyyy",
        "duration": (Integer)
    }
    ```

### `GET /trip/<trip_id>`
- **Description**: Gets specific trip.
- **Response**:
    - Status code 400, if there are no places for the trip.
    - Status code 200, if there are places in the trip.
    ```json
    {
        "dayOrder": [
            "day-1",
            ...
        ],
        "days": {
            "day-1": {
                "dateMMDD": "mm/dd",
                "dateWeekdayMonthDay": "Weekday, Month Day",
                "dateMMDDYYYY": "mm/dd/yyyy",
                "id": "day-1",
                "databaseId": 1,
                "name": ,
                "placeIds": [
                    (Integer),
                    ...
                ],
                "weekday": "Weekday Abbreviation",
            },
            ...
        },
        "places": {
            "1": {
                "address": "",
                "apiId": "",
                "avgVisitTime": (Float),
                "category": "",
                "dayDatabaseId": (Integer),
                "favorite": (Boolean),
                "geocode": [ (Float),(Float) ],
                "databaseId": (Integer, unique identifier for the element in the database),
                "imgUrl": "",
                "inItinerary": (Boolean),
                "info": "",
                "lat": (Float),
                "long": (Float),
                "phoneNumber": "",
                "id": 1 (index of place relative to a trip),
                "name": "",
                "rating": "",
                "summary": "",
                "tripId": (Integer),
                "website": ""
            },
            ...
        },
        "lastPlaceId": (Integer),
        "savedPlaces": {
            "addresses": [ "", ... ],
            "placeIds": [ (Integer), ... ]
        },
        "tripId": (Integer)
    }
    ```

### `GET /trip/trips/<uid>`
- **Description**: Gets all trips for a user.
- **Response**: Status code 200.
    ```json
    [
        {
            "city": "",
            "country": "",
            "countryAbbr": "",
            "imgUrl": "",
            "lat": (Double),
            "long": (Double),
            "state": "",
            "duration": (Integer),
            "endDate": "mm/dd/yyyy",
            "id": (Integer),
            "isItinerary": (Boolean),
            "name": "",
            "startDate": "mm/dd/yyyy",
            "uid": ""
        },
        ...
    ]
    ```

### `DELETE /trip/delete/<trip_id>`
- **Description**: Delete specified trip.
- **Response**: Status code 200, on success.

### `PATCH /trip/update/<trip_id>`
- **Description**: Update trip info.
- **Request Body**:
    ```json
    {
        "tripName": "",
        "startDate": "mm/dd/yyyy",
        "endDate": "mm/dd/yyyy"
    }
    ```
- **Response**:
    - Status code 400, if trip doesn’t exist.
    - Status code 200, if successful and regenerates itinerary.

### `POST /profile/user`
- **Description**: Creates new user.
- **Request Body**:
    ```json
    {
        "uid": "",
        "username": "",
        "email": "",
        "firstName": "",
        "lastName": ""
    }
    ```
- **Response**: 
    ```json
    {
        "email": "",
        "hasAccess": ,
        "uid": "",
        "username" (optional): "",
        "firstName" (optional): "",
        "lastName" (optional): ""
    }
    ```

### `GET /profile/user`
- **Description**: Get user data.
- **Request Body**:
    ```json
    {
        "uid": "",
    }
    ```
- **Response**: 
    - Status code 400, if user exists already.
    - Status code 200, if user successfully added.
    ```json
    {
        "email": "",
        "hasAccess": (Boolean),
        "uid": "",
        "username": "",
        "firstName": "",
        "lastName": ""
    }
    ```

### `PATCH /profile/update`
- **Description**: Updates existing user.
- **Request Body**:
    ```json
    {
        "uid": "",
        "username" (optional): "",
        "email" (optional): "",
        "firstName" (optional): "",
        "lastName" (optional): ""
    }
    ```
- **Response**: 200 or 400 response code.

### `POST|GET /profile/user-info`
- **Description**: Adds user info to user.
- **Request Body**:
    ```json
    GET
    {
        "uid": ""
    }

    POST
    {
        "uid": "",
        "categories": {
            "shopping": (Boolean),
            "nature": (Boolean),
            "landmarks": (Boolean),
            "entertainment": (Boolean),
            "relaxation": (Boolean),
            "food": (Boolean),
            "arts": (Boolean)
        }
    }
    ```
- **Response**:
    - Status code 400, if user has not been created yet.
    - Status code 200, if successfully added user info.
    ```json
    GET
    {
        "uid": "",
        "shopping": (Boolean),
        "nature": (Boolean),
        "landmarks": (Boolean),
        "entertainment": (Boolean),
        "relaxation": (Boolean),
        "food": (Boolean),
        "arts": (Boolean)
    }
    ```