from wtforms import (
    StringField,
    IntegerField,
    ValidationError,
)
from wtforms.validators import (
    Email,
    InputRequired,
    Length,
    EqualTo,
    Regexp,
)

from apps import BaseForm
from .models import FrontUser
from utils import cache, log


class RegisterForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[35678]\d{9}', message='请输入正确的手机号码')])
    username = StringField(validators=[Length(2, 20, message='用户名格式错误')])
    password1 = StringField(validators=[Length(5, 15, message='密码长度应为5-15')])
    password2 = StringField(validators=[EqualTo('password1', message='两次密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='图形验证码错误')])

    def validate_telephone(self, field):
        user = FrontUser.query.filter_by(telephone=field.data).first()
        if user:
            raise ValidationError('该手机号已被注册')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        if graph_captcha is not None:
            # 因为图形验证码存储的key和值都是一样的，所以我们只要判断key是否存在就行
            if cache.get(graph_captcha.lower()) is None:
                raise ValidationError(message='图形验证码错误')


class LoginForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[35678]\d{9}', message='请输入正确的手机号码')])
    password = StringField(validators=[Length(5, 15, message='密码长度应为5-15')])
    remember = StringField()

    def validate_telephone(self, field):
        user = FrontUser.query.filter_by(telephone=field.data).first()
        if user is None:
            raise ValidationError('该手机号未注册')
