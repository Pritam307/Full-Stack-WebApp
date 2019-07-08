from functools import wraps

from flask import flash, redirect, url_for,session
from flask_login import current_user

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.verified is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function


def admin_login(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        if 'username'in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


# def change_status(func):
#     @wraps(func)
#     def wrap(*args, **kwargs):
#         if app.config['IS_VACANT']:
#             