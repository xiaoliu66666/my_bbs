"""
专门用来写一些test demo 的

"""

# 装饰器顺序探索
#
# def decorator_a(func):
#     print('Get in decorator_a')
#
#     def inner_a(*args, **kwargs):
#         print('Get in inner_a')
#         return func(*args, **kwargs)
#
#     return inner_a
#
#
# def decorator_b(func):
#     print('Get in decorator_b')
#
#     def inner_b(*args, **kwargs):
#         print('Get in inner_b')
#         return func(*args, **kwargs)
#
#     return inner_b
#
#
# @decorator_b
# @decorator_a
# def f(x):
#     print('Get in f')
#     return x * 2
#
#
# f(1)

# flask-socketio
#
# import psutil
# import time
# from threading import Lock
# from flask import Flask, render_template
# from flask_socketio import SocketIO
#
# async_mode = None
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()
#
#
# # 后台线程 产生数据，即刻推送至前端
# def background_thread():
#     count = 0
#     while True:
#         socketio.sleep(5)
#         count += 1
#         t = time.strftime('%M:%S', time.localtime())
#         # 获取系统时间（只取分:秒）
#         cpus = psutil.cpu_percent(interval=None, percpu=True)
#         # 获取系统cpu使用率 non-blocking
#         socketio.emit('server_response',
#                       {'data': [t, cpus], 'count': count},
#                       namespace='/test')
#
#
# @app.route('/')
# def index():
#     return render_template('test.html', async_mode=socketio.async_mode)
#
#
# @socketio.on('connect', namespace='/test')
# def test_connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(target=background_thread)
#
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True)
# from functools import wraps
#
# from flask import request, render_template, Flask
#
# from utils.redis_cache import RCache
#
#
# cache = RCache()
# app = Flask(__name__)
#
#
# def cached(timeout=5 * 60, key='view_%s'):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             cache_key = key % request.path
#             value = cache.get_data(cache_key)
#             if value is None:
#                 value = f(*args, **kwargs)
#                 cache.set_data(cache_key, value, ex=timeout)
#             return value
#         return decorated_function
#     return decorator
#
#
# @app.route('/hello')
# @app.route('/hello/<name>')
# @cached()
# def hello(name=None):
#     print('view hello called')
#     return 'hello, {}'.format(name)
#
#
# if __name__ == '__main__':
#     app.run()

# from flask import Flask, jsonify, abort, make_response, request
#
# app = Flask(__name__)
#
# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]
#
#
# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
#
#
# @app.route('/todo/api/v1.0/tasks/<int:tid>', methods=['GET'])
# def get_task(tid):
#     task = list(filter(lambda t: t['id'] == tid, tasks))
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# @app.route('/todo/api/v1.0/tasks', methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

from wsgiref.simple_server import make_server

