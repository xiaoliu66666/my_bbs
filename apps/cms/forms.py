from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length


class LoginForm(Form):
    email = StringField(validators=[Email(message="请输入正确的邮箱格式"),
                                    InputRequired(message="请输入邮箱"),
                                    ])
    password = StringField(validators=[Length(6, 20, message="请输入正确的密码格式")])
    remember = IntegerField()
