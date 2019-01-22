from wtforms import (
    StringField,
    IntegerField,
)
from wtforms.validators import (
    Email,
    InputRequired,
    Length,
    EqualTo,
)

from apps import BaseForm


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式"),
                                    InputRequired(message="请输入邮箱"),
                                    ])
    password = StringField(validators=[Length(6, 20, message="请输入正确的密码格式")])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 30, message='密码长度6-30')])
    newpwd = StringField(validators=[Length(6, 30, message='密码长度6-30')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='新密码输入不一致')])
