import functools
from utils.response_code import RET

from utils.session import Session


def required_login(fun):
    # 保证被装饰的函数对象__name__不变
    @functools.wraps(fun)
    def wrapper(request_handler_obj, *args, **kwargs):
        # 调用get_current_user方法判断用户是否登陆
        if not request_handler_obj.get_current_user():
            request_handler_obj.write(dict(errcode=RET.SESSIONERR, errmsg="用户未登陆"))
        else:
            fun(request_handler_obj, *args, **kwargs)

    return wrapper


