import shortuuid
import enum

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOWN = 4


class FrontUser(db.Model):
    __tablename__ = "front_user"
    # 为了不让他人识别出网站有多少用户，这里采用shortuuid来生成id
    id = db.Column(db.String(50), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOWN)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 登录时先获取密码，再调用check_password验证是否密码一致
    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get("password", "")
            kwargs.pop("password")
        super().__init__(*args, **kwargs)

    # 利用@property装饰器来实现加密密码
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_pwd):
        self._password = generate_password_hash(raw_pwd)

    def check_password(self, raw_pwd):
        result = check_password_hash(self.password, raw_pwd)
        return result

