import psutil
import string
import random
import time

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
from apps.common.models import BannerModel, BoardModel, PostModel, HighlightPostModel
from .decorators import login_required, permission_required
from config import CMS_USER_ID
from exts import db, mail, socketio
from flask_mail import Message
from tasks import send_mail
from threading import Lock

main = Blueprint("cms", __name__, url_prefix="/cms")

thread = None
thread_lock = Lock()


def background_thread():
    # 后台线程 产生数据，即刻推送至前端
    count = 0
    while True:
        socketio.sleep(5)
        count += 1
        t = time.strftime('%H:%M:%S', time.localtime())
        # 获取系统时间（只取时:分:秒）
        cpus = psutil.cpu_percent(interval=None, percpu=True)
        # 获取系统cpu使用率 non-blocking
        socketio.emit('server_response',
                      {'data': [t, cpus], 'count': count},
                      namespace='/test')


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
    # message = Message(
    #     "修改邮箱的验证码",
    #     recipients=[email],
    #     body="验证码是：{}".format(captcha)
    # )
    # try:
    #     mail.send(message)
    # except:
    #     return xjson.server_error("服务器错误")

    # celery 异步发送邮件
    send_mail.delay("修改邮箱的验证码", [email], "验证码是：{}".format(captcha))
    cache.set(email, captcha)
    return xjson.success("发送成功")


@main.route("/profile/")
@login_required
def profile():
    # 个人信息
    return render_template("cms/cms_profile.html")


@main.route("/posts/")
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    posts1 = PostModel.query.order_by(PostModel.create_time.desc())
    return render_template("cms/cms_posts.html", posts=posts1)


@main.route('/hpost/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    # 加精帖子
    post_id = request.form.get("post_id")
    if not post_id:
        return xjson.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return xjson.params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return xjson.success()


@main.route('/uhpost/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    # 取消加精
    post_id = request.form.get("post_id")
    if not post_id:
        return xjson.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return xjson.params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return xjson.success()


@main.route('/dpost/', methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def dpost():
    # 删除帖子
    post_id = request.form.get("post_id")
    if not post_id:
        return xjson.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return xjson.params_error("没有这篇帖子！")

    db.session.delete(post)
    db.session.commit()
    return xjson.success(message="删除帖子成功！")


@main.route("/comments/")
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template("cms/cms_comments.html")


@main.route("/boards/")
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    boards1 = BoardModel.query.all()
    return render_template("cms/cms_boards.html", boards=boards1)


@main.route("/aboard/", methods=["POST"])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    # 添加板块
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
    # 更新板块
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
    # 管理前台用户
    return render_template("cms/cms_fusers.html")


@main.route("/users/")
@login_required
@permission_required(CMSPersmission.CMSUSER)
def users():
    # 管理后台用户
    return render_template("cms/cms_users.html")


@main.route("/roles/")
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def roles():
    # 管理权限
    return render_template("cms/cms_roles.html")


@main.route("/banners/")
@login_required
def banners():
    # 轮播图管理
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template("cms/cms_banners.html", banners=banners)


@main.route("/abanner/", methods=["POST"])
@login_required
def abanner():
    # 添加轮播图
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
    # 更新轮播图
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


@main.route('/cpu/')
def cpu():
    return render_template('cms/cms_cpu.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


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
            if user and user.check_password(password):
                session[CMS_USER_ID] = user.id
                if remember is not None:
                    session.permanent = True
                # log("当前user：", user.__dict__)
                # log("session： ", session)
                return redirect(url_for('.index'))
            else:
                return self.get(message="邮箱或者密码错误！")
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
