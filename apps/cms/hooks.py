from flask import g, session
from .models import CMSUser
from .views import main
from config import CMS_USER_ID


@main.before_request
def before_request():
    if CMS_USER_ID in session:
        user_id = session.get(CMS_USER_ID, -1)
        user = CMSUser.query.get(user_id)
        if user is not None:
            g.cms_user = user
