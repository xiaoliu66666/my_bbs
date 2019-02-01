from flask import (
    Blueprint,
    url_for,
    request,
    render_template,
    views,
    session,
    g,
)

from exts import db
from .models import FrontUser
from apps.common.models import BannerModel, BoardModel, PostModel
from .forms import RegisterForm, LoginForm, AddPostForm
from utils import xjson, safe_url
from config import FRONT_USER_ID
from .decorators import login_required

main = Blueprint("front", __name__)


@main.route("/")
def index():
    # log("request：", request)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    posts = PostModel.query.all()
    params = {
        "banners": banners,
        "boards": boards,
        "posts": posts,
    }
    return render_template('front/front_index.html', **params)


@main.route("/apost/", methods=["GET", "POST"])
def apost():
    if request.method == "GET":
        boards = BoardModel.query.all()
        return render_template("front/front_apost.html", boards=boards)
    else:
        add_post_form = AddPostForm(request.form)
        if add_post_form.validate():
            title = add_post_form.title.data
            content = add_post_form.content.data
            board_id = add_post_form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return xjson.params_error(message='没有这个板块')
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return xjson.success()
        else:
            return xjson.params_error(message=add_post_form.get_error())


class RegisterView(views.MethodView):
    def get(self):
        # log("host_url: ", request.host_url)
        return_to = request.referrer
        if return_to and return_to != request.url and safe_url.is_safe_url(return_to):
            return render_template('front/front_register.html', return_to=return_to)
        else:
            return render_template('front/front_register.html')

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return xjson.success('恭喜您，注册成功')
        else:
            error = form.get_error()
            # log("error: ", error)
            return xjson.params_error(message=error)


class LoginView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if (return_to is not None
                and return_to != request.url
                and return_to != url_for('front.register')
                and safe_url.is_safe_url(return_to)):
            return render_template('front/front_login.html', return_to=return_to)
        else:
            return render_template('front/front_login.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[FRONT_USER_ID] = user.id
                if remember is not None:
                    session.permanent = True
                return xjson.success()
            else:
                return xjson.params_error(message="手机号或者密码错误")
        else:
            return xjson.params_error(message=form.get_error())


main.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
main.add_url_rule('/login/', view_func=LoginView.as_view('login'))
