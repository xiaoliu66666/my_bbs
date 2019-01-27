from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    views,
    make_response,
)
from io import BytesIO
from utils.captcha import Captcha


main = Blueprint("front", __name__)


@main.route("/")
def index():
    return "front index"


class RegisterView(views.MethodView):
    def get(self):
        return render_template('front/front_register.html')

    def post(self):
        ...


main.add_url_rule('/register/', view_func=RegisterView.as_view('register'))


