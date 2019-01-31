from functools import wraps

from flask import session, url_for
from werkzeug.utils import redirect

from config import FRONT_USER_ID


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('.login'))
    return inner
