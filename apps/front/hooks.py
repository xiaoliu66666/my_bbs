"""
在request上下文中添加一个g.front_user的全局变量
"""
from .views import main
from config import FRONT_USER_ID
from flask import session, g
from .models import FrontUser


@main.before_request
def my_before_request():
    if FRONT_USER_ID in session:
        user_id = session.get(FRONT_USER_ID, -1)
        user = FrontUser.query.get(user_id)
        if user:
            g.front_user = user
