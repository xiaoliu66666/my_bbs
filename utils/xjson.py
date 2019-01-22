from flask import jsonify


class StatusCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data or {}})


def success(message='', data=None):
    return result(code=StatusCode.ok, message=message, data=data)


def params_error(message='', data=None):
    """
     请求参数错误
    """
    return result(code=StatusCode.paramserror, message=message, data=data)


def unauth_error(message='', data=None):
    """
    没有权限访问
    """
    return result(code=StatusCode.unauth, message=message, data=data)


def method_error(message='', data=None):
    """
    请求方法错误
    """
    return result(code=StatusCode.methoderror, message=message, data=data)


def server_error(message='', data=None):
    """
    服务器内部错误
    """
    return result(code=StatusCode.servererror, message=message, data=data)
