import memcache

mc = memcache.Client(["127.0.0.1:11211"], debug=True)


def set(k, v, timeout=60):
    return mc.set(k, v, time=timeout)


def get(k):
    return mc.get(k)


def set_multi(timeout=60, **kwargs):
    return mc.set_multi(kwargs, time=timeout)


def delete(k):
    return mc.delete(k)
