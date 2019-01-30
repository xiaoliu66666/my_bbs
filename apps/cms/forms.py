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
)

from apps import BaseForm
from utils import cache, log
from .models import CMSUser


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


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱")])
    captcha = StringField(validators=[Length(6, 6, message='验证码长度不符')])

    def validate_captcha(self, filed):
        captcha = filed.data.lower()
        email = self.email.data
        captcha_cache = cache.get(email).lower()
        if captcha_cache is None or captcha_cache != captcha:
            raise ValidationError("验证码错误")

    def validate_email(self, field):
        user = CMSUser.query.filter_by(email=field.data).first()
        # log("user.email：", user.email, "表单中的email：", email)
        if user is not None:
            raise ValidationError("邮箱重复")


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id！')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！')])


class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])
