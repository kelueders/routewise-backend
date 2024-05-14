from functools import wraps
import os
from flask import flash, redirect, render_template, request, session, url_for


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