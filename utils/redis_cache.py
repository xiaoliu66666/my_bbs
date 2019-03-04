"""
利用pickle包将data序列化，然后存入redis中
思路是来自于 werkzeug 库的 contrib.cache.RedisCache
"""
from functools import wraps

import redis
import pickle
# from werkzeug.contrib.cache import RedisCache
from flask import request


class RCache:
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    @staticmethod
    def set_data(key, data, ex=None):
        # 将内存数据转化成文本流并存入redis
        _data = pickle.dumps(data)
        RCache.redis_db.set(key, _data, ex)

    @staticmethod
    def get_data(key):
        # 从redis中获取数据并反序列化，返回数据
        data = RCache.redis_db.get(key)
        if not data:
            return None

        return pickle.loads(data)


cache = RCache()


def cached(timeout=None, key='view_%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            value = cache.get_data(cache_key)
            if value is None:
                value = f(*args, **kwargs)
                cache.set_data(cache_key, value, ex=timeout)
            return value
        return decorated_function
    return decorator