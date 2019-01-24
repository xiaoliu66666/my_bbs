import string
import random

from flask import (
    Blueprint,
    render_template,
    views,
    request,
    redirect,
    url_for,
    session,
    g,
)

from utils import log, xjson
from .forms import LoginForm, ResetPwdForm
from .models import CMSUser
from .decorators import login_required
from config import CMS_USER_ID
from exts import db, mail
from flask_mail import Message


main = Blueprint("cms", __name__, url_prefix="/cms")


@main.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")


@main.route("/email_captcha/")
@login_required
def email_captcha():
    # url 应该是：/email_captcha/?email=xxxxx
    email = request.args.get('email')
    if email is None:
        return xjson.params_error("邮箱为空")

    # 成功传入email参数
    s = list(string.ascii_letters)
    s.extend([str(i) for i in range(0, 10)])
    captcha = "".join(random.sample(s, 6))
    message = Message(
        "修改邮箱的验证码",
        recipients=[email],
        body="验证码是：{}".format(captcha)
    )

    try:
        mail.send(message)
    except:
        return xjson.server_error("服务器错误")

    return xjson.success("发送成功")


@main.route("/profile/")
@login_required
def profile():
    return render_template("cms/cms_profile.html")


@main.route("/logout/")
@login_required
def logout():
    del session[CMS_USER_ID]
    return redirect(url_for('.login'))


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template("cms/cms_login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            # todo： 这一部分应该可以放在model中实现
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session[CMS_USER_ID] = user.id
                if remember is not None:
                    session.permanent = True
                # log("当前user：", user.__dict__)
                # log("session： ", session)
                return redirect(url_for('.index'))
            else:
                return self.get(message="邮箱或者密码错误！")
                # flash("邮箱或者密码错误")
                # return redirect(url_for('.index'))
        else:
            # log("form.error", form.errors)
            # form.errors 返回的是一个字典，
            # popitem方法返回的是一个装着键值对的tuple，第二个元素是用list存储的错误信息
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # 因为接受的是ajax,所以这里使用jsonify返回数据
                # 返回code字段表示状态码，message信息提示
                return xjson.success("修改成功")
            else:
                return xjson.params_error("原密码错误")
        else:
            message = form.get_error()
            return xjson.params_error(message)


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetemail.html")

    def post(self):
        ...


main.add_url_rule("/login/", view_func=LoginView.as_view("login"))
main.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view("resetpwd"))
main.add_url_rule("/resetemail/", view_func=ResetEmailView.as_view("resetemail"))
