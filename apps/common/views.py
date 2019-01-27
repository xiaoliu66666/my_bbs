from io import BytesIO

from flask import Blueprint, make_response

from utils.captcha import Captcha
from utils import cache

main = Blueprint("common", __name__, url_prefix="/common")


@main.route("/")
def index():
    return "common index"


@main.route("/captcha/")
def graph_capcha():
    text, image = Captcha.gene_graph_captcha()
    # 将图形验证码按照 文本：文本的格式存储到memcache中
    cache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp
