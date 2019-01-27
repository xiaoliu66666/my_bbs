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


@main.route("/captcha/")
def graph_capcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


class RegisterView(views.MethodView):
    def get(self):
        return render_template('front/front_register.html')

    def post(self):
        ...


main.add_url_rule('/register/', view_func=RegisterView.as_view('register'))


