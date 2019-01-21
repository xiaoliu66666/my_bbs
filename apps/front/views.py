from flask import Blueprint


main = Blueprint("front", __name__)


@main.route("/")
def index():
    return "front index"
