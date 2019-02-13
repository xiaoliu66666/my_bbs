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


