from flask import (
    Blueprint,
    render_template,
)

main = Blueprint('error', __name__)


@main.app_errorhandler(404)
def error(e):
    return render_template("common/page_not_found.html")


@main.app_errorhandler(500)
def error(e):
    return render_template("common/internal_server_error.html")

