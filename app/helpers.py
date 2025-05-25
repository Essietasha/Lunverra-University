from functools import wraps
from flask import redirect, render_template, session, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userID' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function