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

from utils import xjson, cache
from .forms import (
    LoginForm,
    ResetPwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm,
)
from .models import CMSUser, CMSPersmission
from apps.common.models import BannerModel, BoardModel
from .decorators import login_required, permission_required
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

    cache.set(email, captcha)
    return xjson.success("发送成功")


@main.route("/profile/")
@login_required
def profile():
    return render_template("cms/cms_profile.html")


@main.route("/posts/")
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    return render_template("cms/cms_posts.html")


@main.route("/comments/")
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template("cms/cms_comments.html")


@main.route("/boards/")
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    boards = BoardModel.query.all()
    return render_template("cms/cms_boards.html", boards=boards)


@main.route("/aboard/", methods=["POST"])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return xjson.success()
    else:
        return xjson.params_error(form.get_error())


@main.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        if board_id:
            board = BoardModel.query.get(board_id)
            board.name = name
            db.session.commit()
            return xjson.success(message='更新成功')
        else:
            return xjson.params_error(message='板块不存在')
    else:
        return xjson.params_error(message=form.get_error())


@main.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return xjson.params_error(message='请传入板块id')
    board = BoardModel.query.get(board_id)
    if not board:
        return xjson.params_error(message='没有这个板块')

    db.session.delete(board)
    db.session.commit()
    return xjson.success(message='删除板块成功')


@main.route("/fusers/")
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template("cms/cms_fusers.html")


@main.route("/users/")
@login_required
@permission_required(CMSPersmission.CMSUSER)
def users():
    return render_template("cms/cms_users.html")


@main.route("/roles/")
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def roles():
    return render_template("cms/cms_roles.html")


@main.route("/banners/")
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template("cms/cms_banners.html", banners=banners)


@main.route("/abanner/", methods=["POST"])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return xjson.success()
    else:
        return xjson.params_error(message=form.get_error())


@main.route("/ubanner/", methods=["POST"])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner is not None:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return xjson.success()
        else:
            return xjson.params_error(message="没有这个轮播图!")
    else:
        return xjson.params_error(message=form.get_error())


@main.route("/dbanner/", methods=["POST"])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    banner = BannerModel.query.get(banner_id)
    if banner is not None:
        db.session.delete(banner)
        db.session.commit()
        return xjson.success()
    else:
        return xjson.params_error("没有这个轮播图")


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
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return xjson.success("修改邮箱成功")
        else:
            msg = form.get_error()
            return xjson.params_error(msg)


main.add_url_rule("/login/", view_func=LoginView.as_view("login"))
main.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view("resetpwd"))
main.add_url_rule("/resetemail/", view_func=ResetEmailView.as_view("resetemail"))
