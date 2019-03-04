from flask import (
    Blueprint,
    url_for,
    request,
    render_template,
    views,
    session,
    g,
    abort,
    redirect,
)
from sqlalchemy import func

from exts import db
from .models import FrontUser
from apps.common.models import (
    BannerModel,
    BoardModel,
    PostModel,
    CommentModel,
    HighlightPostModel,
)
from .forms import RegisterForm, LoginForm, AddPostForm, AddCommentForm
from utils import xjson, safe_url, spider, log
from utils.redis_cache import cached
from config import FRONT_USER_ID, PER_PAGE, EXPIRE_CACHED_PAGE_TO_REDIS
from .decorators import login_required
from flask_paginate import get_page_parameter, Pagination
from exts import collections

import threading

main = Blueprint("front", __name__)


@main.route("/")
@cached(timeout=EXPIRE_CACHED_PAGE_TO_REDIS)
def index():
    # log("request：", request)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()

    # 根据当前页码来进行分页
    current_page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (current_page - 1) * PER_PAGE
    end = start + PER_PAGE

    # 帖子排序
    sort = request.args.get("st", type=int, default=1)
    if sort == 1:
        # 默认排序:按照发布时间倒序
        query = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒序
        query = db.session.query(PostModel).join(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc())
    elif sort == 3:
        # 按照阅读的数量排序,
        # todo:点赞功能还没有做
        query = PostModel.query.order_by(PostModel.view_count.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    # 根据板块显示帖子
    board_id = request.args.get("bid", type=int, default=None)
    if board_id is not None:
        query = PostModel.query.filter_by(board_id=board_id)
        posts = query.slice(start, end)
        total = query.count()
    else:
        posts = query.slice(start, end)
        total = query.count()
    paginate = Pagination(bs_version=3, outer_window=0,
                          total=total,
                          page=current_page)
    params = {
        "banners": banners,
        "boards": boards,
        "posts": posts,
        "paginate": paginate,
        "current_board": board_id,
        "current_sort": sort,
    }
    return render_template('front/front_index.html', **params)


@main.route('/acomment/', methods=['POST'])
@login_required
def acomment():
    # 添加评论
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            # 如果帖子存在，就把评论写入数据库
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return xjson.success()
        else:
            return xjson.params_error('没有这篇帖子！')
    else:
        return xjson.params_error(form.get_error())


@main.route("/p/<pid>")
@cached(timeout=EXPIRE_CACHED_PAGE_TO_REDIS)
def detail(pid):
    # 帖子详情页面
    # log("request path:", request.path)
    post = PostModel.query.get(pid)
    comments = CommentModel.query.filter_by(post_id=pid)
    counts = comments.count()
    post.view_count += 1
    db.session.commit()
    if post is None:
        abort(404)
    params = {
        "post": post,
        "comments": comments,
        "counts": counts,
    }
    return render_template("front/front_detail.html", **params)


@main.route("/apost/", methods=["GET", "POST"])
@login_required
def apost():
    # 添加帖子
    if request.method == "GET":
        if "front_user" not in g.__dict__:
            return redirect(url_for('.login'))
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
            # 作者等于当前登录的用户
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return xjson.success()
        else:
            return xjson.params_error(message=add_post_form.get_error())


@main.route("/logout/")
@login_required
def logout():
    del session[FRONT_USER_ID]
    return redirect(url_for('.index'))


@main.route("/movies/")
@login_required
def movies():
    # 电影板块
    _movies = collections.find().limit(10)
    return render_template('front/front_movies.html', movies=_movies)


@main.route("/new/", methods=["GET", "POST"])
@login_required
def new():
    # 开始后台爬取电影
    t = threading.Thread(target=spider.spider)
    t.setDaemon(True)
    t.start()
    return redirect(url_for('.movies'))


class RegisterView(views.MethodView):
    def get(self):
        # log("host_url: ", request.host_url)
        # return_to为前一个跳转页面
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
        # return_to 不能为当前页面，也不能为注册页面，并且要确保是安全的url
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
                # 如果用户存在就把user.id写入session
                session[FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return xjson.success()
            else:
                return xjson.params_error(message="手机号或者密码错误")
        else:
            return xjson.params_error(message=form.get_error())


main.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
main.add_url_rule('/login/', view_func=LoginView.as_view('login'))
