from flask import Flask
import config
from exts import db
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from apps.cms import main as cms
    from apps.front import main as front
    from apps.common import main as common

    app.register_blueprint(cms)
    app.register_blueprint(common)
    app.register_blueprint(front)

    db.init_app(app)
    CSRFProtect(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)


