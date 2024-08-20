# RouteWise Backend
The backend includes the api endpoints for the frontend to access the database and includes the algorithm for creating an itinerary. The project is built using the Flask framework in Python. The backend is hosted on Render. For data management, the project uses PostgreSQL.

### Tech Stack
- Python
- Flask Framework
- PostgreSQL
- Render
- Docker

## How to Run and Test
1. Install the dependencies. **Note**: you may need to comment out some depenencies and manually install it.

    ``` 
    pip install -r requirements.txt 
    ```

2. Set config variables for the flask app as environment variables. Create `.env` file in the root directory and fill with the following data. Replace '****' with the secret.
    ```
    FLASK_APP = app
    FLASK_ENV = development
    FLASK_DEBUG = true
    SECRET_KEY = '****'
    SQLALCHEMY_DATABASE_URI = ****
    PASSCODE = '****'
    ```

3. Run the program. This will launch the test environment on port 5000.

    ` flask run `

### UPDATE: Run in docker container
Running the program in a docker container ensures it runs in a clean enviornment. The environment is specified in dockerfile.

1. Install docker on your machine following the instructions on [docker](https://www.docker.com/)

2. Navigate to the directory with the dockerfile. Build the image with the tag flask-run. Make sure docker is running in the background.

    `docker build -t flask-run .`

3. Run the image with the -d tag to have the container running in the background and -p localhost:8000 to connect with the port. This will allow users to access the routes using port 8000.

    `docker run -dp 127.0.0.1:8000:5000 flask-run`

4. View if the container is active and running

    `docker ps`

5. To access the workspace inside the container, exec into the container using a shell space.

    `docker exec -it container_id sh`

4. Stop a running docker container, replace container_id with the actual ID that can be found by running the `docker ps` command.

    `docker stop container_id`

## Code Structure
- /app : The Flask code is contained in the app directory. It also initiates the webpage for port 5000.
    - models.py : contains the schema for database models.
    - global_helpers.py : contains helper functions used in multiple files.
    - /auth : contains the api route to handle granting access to a user
    - /itinerary : contains the algorithm to create an itinerary and the api routes to manipulate an itinerary.
    - /places : contains the api routes to handle getting and manipulating trip and places data from the database.
    - /profile : contains the api route to handle getting and manipulating user data in the database.
- / : outlines the necessary requirements to run the program

## API Documentation

### `GET|PATCH /auth/check_code`
- **Description**: Verify user access.
- **Request Body**:
    ```json
    {
        "uid": "",
        "passcode": ""
    }
    ```
- **Response**: code 200, "Access granted" or "Access not granted".

### `GET|PATCH /itinerary/createdays/<trip_id>`
- **Description**: 
- **Response**: 

### `POST|GET /itinerary/add-one-place/<trip_id>`
- **Description**: 
- **Request Body**:
- **Response**: 

### `DELETE /itinerary/delete-place/<place_id>`
- **Description**: Deletes place.
- **Response**: 

### `PATCH /itinerary/update-place/<place_id>`
- **Description**: 
- **Request Body**:
- **Response**: 

### `POST|GET /places/trip`
- **Description**: Adds a new empty trip.
- **Request Body**:
  ```json
  {
    "uid": "",
    "tripData": {
      "tripName": "",
      "cityName": "",
      "state": "",
      "country": "",
      "country_2letter": "",
      "destinationLat": ,
      "destinationLong": ,
      "destinationImg": "",
      "startDate": "",
      "endDate": ""
    }
  }
  ```
- **Response**:
  ```json
  {
    "trip_id": ,
    "start_date": "",
    "end_date": "",
    "duration":
  }
  ```

### `GET /places/trip/<trip_id>`
- **Description**: Gets specific trip.
- **Response**: 
    ```json
    {
        "day_order": [
            "day-1"
        ],
        "days": {
            "day-1": {
                "date_converted": "",
                "date_short": "",
                "dayName": "",
                "day_short": "",
                "db_id": ,
                "id": "day-1",
                "placeIds": [
                ]
            }
        },
        "places": {
            "1": {
                "address": "",
                "day_id": ,
                "favorite": false,
                "geocode": [
                ],
                "id": 1,
                "imgURL": "",
                "info": "",
                "lat": ,
                "long": ,
                "placeName": "",
                "place_id":
            }
        },
        "places_last": ,
        "saved_places": {
            "addresses": [
            ],
            "placesIds": [
            ]
        },
        "trip_id": 
    }
    ```

### `DELETE /places/delete-trip/<trip_id>`
- **Description**: Delete specified trip.
- **Response**: Success or error message.

### `PATCH|POST|GET|DELETE /places/update-trip/<trip_id>`
- **Description**: Update trip info.
- **Request Body**:
    ```json
    {
        "tripName": "",
        "startDate": "",
        "endDate": ""
    }
    ```

### `POST /places/add-place/<trip_id>`
- **Description**: Add place to trip.
- **Request Body**:
    ```json
    {
        "tripId": ,
        "placesLast": ,
        "places_serial": [
            {
                "id": 1,
                "placeName": "",
                "placeId": "",
                "address": "",
                "imgURL": "",
                "category": "",
                "favorite": false,
                "info": "",
                "lat": ,
                "long": 
            }
        ]
    }
    ```

### `GET /places/get-places/<trip_id>`
- **Description**: Gets places in trip.
- **Response**: 
    ```json
    [
        {
            "category": "",
            "favorite": ,
            "geoapify_placeId": "",
            "in_itinerary": true,
            "info": "",
            "lat": ,
            "local_id": ,
            "long": ,
            "place_address": "",
            "place_id": ,
            "place_img": "",
            "place_name": "",
            "trip_id": 
        }
    ]
    ```

### `GET|POST /places/add-get-place/<trip_id>`
- **Description**: Add a place to empty itinerary.
- **Request Body**:
    ```json
    {
        "id": ,
        "placeName": "",
        "placeId": "",
        "address": "",
        "imgURL": "",
        "category": "",
        "favorite": false,
        "info": "",
        "lat": ,
        "long":
    }
    ```
- **Response**: Place ID.

### `GET|POST /places/add-trip-and-places`
- **Description**: Add a new trip with places.
- **Request Body**:
    ```json
    {
        "uid": "",
        "currentTrip": {
            "tripName": "",
            "city": "",
            "state": "",
            "country": "",
            "country_2letter": "",
            "geocode": [],
            "imgUrl": "",
            "startDate": "",
            "endDate": "",
            "places": [
                {
                    "id": 1,
                    "placeName": "",
                    "placeId": "",
                    "address": "",
                    "imgURL": "",
                    "category": "",
                    "favorite": false,
                    "info": "",
                    "lat": ,
                    "long": 
                }
            ]
        }
    }
    ```

### `POST /profile/user`
- **Description**: Creates new user.
- **Request Body**:
    ```json
    {
        "uid": "",
        "displayName": "",
        "email": ""
    }
    ```
- **Response**: 
    ```json
    {
        "email": "",
        "has_access": ,
        "uid": "",
        "username": ""
    }
    ```

### `POST|GET /profile/user_info`
- **Description**: Adds user info to user.
- **Request Body**:
    ```json
    {
        "uid": "",
        "categories": {
            "shopping": ,
            "nature": ,
            "landmarks": ,
            "entertainment": ,
            "relaxation": ,
            "food": ,
            "arts": 
        }
    }
    ```