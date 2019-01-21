from flask import Blueprint


main = Blueprint("cms", __name__, url_prefix="/cms")


@main.route("/")
def index():
    return "cms index"


