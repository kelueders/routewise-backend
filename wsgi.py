from app import app

'''
Web Server Gateway Interface

This file acts as en entry point for deploying the flask app in a 
production environment. The environment will run on Gunicorn.

'''
if __name__ == '__main__':
    app.run()