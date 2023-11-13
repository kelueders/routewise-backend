import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class Config():
    """
        Set Config variables for the flask app.
    """
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    # or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Turn off messages for updates in sqlalchemy