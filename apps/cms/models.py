from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPersmission(object):
    # 255的二进制方式表示11111111
    ALL_PERMISSION = 0b11111111
    # 访问者权限
    VISITOR = 0b00000001
    # 管理帖子权限
    POSTER = 0b00000010
    # 管理评论的权限
    COMMENTER = 0b00000100
    # 管理板块的权限
    BOARDER = 0b00001000
    # 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 管理后台用户的权限
    CMSUSER = 0b00100000
    # 管理后台管理员的权限
    ADMIN = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


class CMSRole(db.Model):
    __tablename__ = "cms_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPersmission.VISITOR)
    # 这里secondary参数是用于多对多关系, 它的值就是关联表的名字,
    # backref参数是给user增加一个roles的属性，使用列表存储
    # 以后就可以用user.roles来获取 CMSRole id属性 的列表
    users = db.relationship("CMSUser", secondary=cms_role_user, backref='roles')


class CMSUser(db.Model):
    __tablename__ = "cms_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_pwd):
        self._password = generate_password_hash(raw_pwd)

    def check_password(self, raw_pwd):
        result = check_password_hash(self.password, raw_pwd)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0

        all_permissions = 0
        for role in self.roles:
            permission = role.permissions
            all_permissions |= permission
        return all_permissions

    def has_permission(self, permission):
        # 将传进去的权限跟用户的所有权限进行 与 运算,
        # 如果结果依旧等于传进去的权限, 则说明拥有这个权限
        return permission & self.permissions == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPersmission.ALL_PERMISSION)


