from flask import Flask
import config


app = Flask(__name__)
app.config.from_object(config)

from apps.cms import main as cms
from apps.front import main as front
from apps.common import main as common

app.register_blueprint(cms)
app.register_blueprint(common)
app.register_blueprint(front)


if __name__ == '__main__':
    app.run(port=8000)


