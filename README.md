# RouteWise Backend
The project is built using the Flask framework in Python. The backend is hosted on Render. For data management, the project uses PostgreSQL.

## How to Run and Test
1. Install the dependencies. Note: you may need to comment out some depenencies and manually install it.

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

## Code Structure
- /app : The Flask code is contained in the app directory. It also initiates the webpage for port 5000.
    - models.py : contains the schema for database models.
    - global_helpers.py : contains helper functions used in multiple files.
    - /auth : contains the api route to handle granting access to a user
    - /itinerary : contains the algorithm to create an itinerary and the api routes to manipulate an itinerary.
    - /places : contains the api routes to handle getting and manipulating trip and places data from the database.
    - /profile : contains the api route to handle getting and manipulating user data in the database.
- / : outlines the necessary requirements to run the program