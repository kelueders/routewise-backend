# RouteWise Backend
The backend includes the api endpoints for the frontend to access the database and includes the algorithm for creating an itinerary. The project is built using the Flask framework in Python. The backend is hosted on Render. For data management, the project uses PostgreSQL.

### Tech Stack
- Python
- Flask Framework
- PostgreSQL
- AWS RDS for PostrgreSQL
- Render (Python version: 3.11.9)
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

    ``` 
    flask run 
    ```

### UPDATE: Run in docker container
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
- **Description**: Create itinerary for places and creates corresponding days.
- **Response**: 
    ```json
    {
        "day_order": [
            "day-1"
        ],
        "days": {
            "day-1": {
                "date_converted": "",
                "date_formatted": "",
                "date_short": "",
                "dayName": "",
                "day_id": ,
                "day_short": "",
                "id": "day-1",
                "placeIds": [
                    
                ]
            }
        },
        "places": {
            "1": {
                "address": "",
                "apiPlaceId": "",
                "avgVisitTime": ,
                "category": "",
                "day_id": ,
                "favorite": ,
                "geocode": [
                    
                ],
                "id": 1,
                "imgURL": "",
                "in_itinerary": true,
                "info": "",
                "lat": ,
                "long": ,
                "phoneNumber": ,
                "placeName": "",
                "place_id": ,
                "rating": "",
                "summary": "",
                "website": 
            }
        },
        "places_last": ,
        "saved_places": {
            "addresses": [],
            "placesIds": []
        },
        "trip_id": ""
    }
    ```

### `POST|GET /itinerary/add-one-place/<trip_id>`
- **Description**: Adds new place if itinerary hasn't been created.
- **Request Body**:
    ```json
    {
        "day_id": null,
        "place":{
            "id": ,
            "placeName": "",
            "info": "",
            "summary": "",
            "address": "",
            "phoneNumber": "",
            "website": "",
            "imgURL": "",
            "category": "",
            "favorite": false,
            "lat": ,
            "long": ,
            "geocode": [
                ,
                
            ],
            "placeId": "",
            "rating": ""
        }
    }
    ```
- **Response**: Place id in list.

### `DELETE /itinerary/delete-place/<place_id>`
- **Description**: Deletes place in its entirety.
- **Response**: Success message

### `DELETE /itinerary/delete-places`
- **Description**: Deletes multiple places at once.
- **Request Body**:
    ```json
    {
        "placeIds": []
    }
    ```
- **Response**: Success message

### `DELETE /itinerary/delete-all-places/<trip_id>`
- **Description**: Deletes all places related to a specified trip.
- **Response**: Success message

### `PATCH /itinerary/update-place/<place_id>`
- **Description**: Updates place specified.
- **Request Body**:
    ```json
    {
        "day_id": ,
        "in_itinerary": false
    }
    ```
- **Response**: Success message

### `PATCH /itinerary/move-day-places/<trip_id>`
- **Description**: Moves/swaps all places in a day to a destination day.
- **Request Body**:
    ```json
    {
        "sourceDayId": ,
        "destDayId" : ,
        "swap": true
    }
    ```
- **Response**: success message

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
                "apiPlaceId": "",
                "avgVisitTime": ,
                "category": "",
                "day_id": ,
                "favorite": false,
                "geocode": [
                ],
                "id": 1,
                "imgURL": "",
                "info": "",
                "lat": ,
                "long": ,
                "phoneNumber": "",
                "placeName": "",
                "place_id": ,
                "rating": "",
                "summary": "",
                "website": ""
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

### `PATCH /places/update-day-name/<day_id>`
- **Description**: Update day name (user created title for a trip day).
- **Request Body**:
    ```json
    {
        "dayName": ""
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
                "phoneNumber": "",
                "rating": "",
                "summary": "",
                "website": "",
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
    {
        "1": {
            "address": "",
            "apiPlaceId": "",
            "avgVisitTime": 60.0,
            "category": "",
            "day_id": ,
            "favorite": false,
            "geocode": [ , ],
            "imgURL": "",
            "in_itinerary": true,
            "info": "",
            "lat": ,
            "local_id": 1,
            "long": ,
            "phoneNumber": "",
            "placeName": "",
            "place_id": ,
            "rating": "",
            "summary": "",
            "website": ""
        }
    }
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
        "phoneNumber": "",
        "rating": "",
        "summary": "",
        "website": "",
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
                    "phoneNumber": "",
                    "rating": "",
                    "summary": "",
                    "website": "",
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
    ```json
    {
        "email": "",
        "hasAccess": ,
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