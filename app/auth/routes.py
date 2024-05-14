from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import os

from app.auth.helpers import check_pw

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='auth_templates')

@auth.route('/test', methods=['GET','POST'])
@check_pw
def test():
    return render_template('test.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    site_password = os.getenv('SITE_PASSWORD')

    if request.method == "POST":
    
        req = request.form
    
        password = req.get("password")
    
    if password != site_password:
        flash('wrong password! try again...')
        return redirect(request.url)
    
    if session["status"] == 'good':
        return redirect(url_for("index"))

    return render_template('login.html')