from flask import (
    Blueprint,
    request,
    jsonify,
    url_for,
    send_from_directory,
    current_app as app
)
import json
import re
import string
import time
import hashlib
import random
import base64
import sys
import os
from urllib import parse

main = Blueprint('ueditor', __name__, url_prefix='/ueditor')

UEDITOR_UPLOAD_PATH = ""


@main.before_app_first_request
def before_first_request():
    global UEDITOR_UPLOAD_PATH
    UEDITOR_UPLOAD_PATH = app.config.get('UEDITOR_UPLOAD_PATH')
    if UEDITOR_UPLOAD_PATH is not None and not os.path.exists(UEDITOR_UPLOAD_PATH):
        os.mkdir(UEDITOR_UPLOAD_PATH)
    csrf = app.extensions.get('csrf')
    if csrf:
        csrf.exempt(upload)


def _random_filename(rawfilename):
    letters = string.ascii_letters
    random_filename = str(time.time()) + "".join(random.sample(letters, 5))
    filename = hashlib.md5(random_filename.encode('utf-8')).hexdigest()
    subffix = os.path.splitext(rawfilename)[-1]
    return filename + subffix


@main.route('/upload/', methods=['GET', 'POST'])
def upload():
    action = request.args.get('action')
    result = {}
    if action == 'config':
        config_path = os.path.join(main.static_folder or app.static_folder, 'ueditor', 'config.json')
        with open(config_path, 'r', encoding='utf-8') as fp:
            result = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))

    elif action in ['uploadimage', 'uploadvideo', 'uploadfile']:
        image = request.files.get("upfile")
        filename = image.filename
        save_filename = _random_filename(filename)
        result = {
            'state': '',
            'url': '',
            'title': '',
            'original': ''
        }
        image.save(os.path.join(UEDITOR_UPLOAD_PATH, save_filename))
        result['state'] = "SUCCESS"
        result['url'] = url_for('ueditor.files', filename=save_filename)
        result['title'] = save_filename,
        result['original'] = image.filename

    elif action == 'uploadscrawl':
        base64data = request.form.get("upfile")
        img = base64.b64decode(base64data)
        filename = _random_filename('xx.png')
        filepath = os.path.join(UEDITOR_UPLOAD_PATH, filename)
        with open(filepath, 'wb') as fp:
            fp.write(img)
        result = {
            "state": "SUCCESS",
            "url": url_for('files', filename=filename),
            "title": filename,
            "original": filename
        }
    return jsonify(result)


@main.route('/files/<filename>/')
def files(filename):
    return send_from_directory(UEDITOR_UPLOAD_PATH, filename)
