from functools import wraps
import os
from flask import app, flash, redirect, render_template, request, session, url_for


site_password = os.getenv('SITE_PASSWORD')

# custom decorator to check password
def check_pw(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        status = session.get('status')
        if status != "good":
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET','POST'])
@check_pw
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
    
        req = request.form
    
        password = req.get("password")
    
    if password != site_password:
        flash('wrong password! try again...')
        return redirect(request.url)
    
    if session["status"] == 'good':
        return redirect(url_for("index"))

    return render_template('login.html')