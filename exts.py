from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect


db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()

csrf = CSRFProtect()