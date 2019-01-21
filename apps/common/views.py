from flask import Blueprint


main = Blueprint("common", __name__, url_prefix="/common")


@main.route("/")
def index():
    return "common index"
