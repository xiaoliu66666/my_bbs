from flask import (
    session,
    redirect,
    url_for,
    g,
)

from functools import wraps

from config import CMS_USER_ID


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('.login'))
    return inner


def permission_required(permission):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('.index'))
        return inner
    return outer
