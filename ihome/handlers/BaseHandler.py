from tornado.web import RequestHandler, StaticFileHandler
from utils.session import Session

import json


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = []

    def write_error(self, status_code: int, **kwargs):
        pass

    def set_default_headers(self):
        pass

    def initialize(self):
        pass

    def on_finish(self):
        pass

    def set_default_handlers(self):
        """设置默认json格式"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def get_current_user(self):
        """判断用户是否登陆"""
        self.session = Session(self)
        return self.session.data


class StaticFileBaseHandler(StaticFileHandler):
    """自定义静态文件处理类, 在用户获取html页面的时候设置_xsrf的cookie"""

    def __init__(self, *args, **kwargs):
        super(StaticFileBaseHandler, self).__init__(*args, **kwargs)
        self.xsrf_token
