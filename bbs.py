from flask import Flask
import config
from exts import db, mail, socketio, csrf

async_mode = None


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from apps.cms import main as cms
    from apps.front import main as front
    from apps.common import main as common
    from apps.ueditor import main as ueditor
    from apps.error import main as error

    app.register_blueprint(cms)
    app.register_blueprint(common)
    app.register_blueprint(front)
    app.register_blueprint(ueditor)
    app.register_blueprint(error)

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app, async_mode=async_mode)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)


