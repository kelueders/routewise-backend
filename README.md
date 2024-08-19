# RouteWise Backend
The backend includes the api endpoints for the frontend to access the database and includes the algorithm for creating an itinerary. The project is built using the Flask framework in Python. The backend is hosted on Render. For data management, the project uses PostgreSQL.

### Tech Stack
- Python
- Flask Framework
- PostgreSQL
- Render

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