import pymongo
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect


db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()

csrf = CSRFProtect()

# 获取连接mongodb的对象
client = pymongo.MongoClient("127.0.0.1", port=27017)

# 获取数据库，即使不存在也没关系
my_db = client.movies
# 获取数据库中的集合（对应mysql中的表）
collections = my_db.new_movies

