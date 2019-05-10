import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import options, define

from apps.urls import urls
from apps.configs import configs

define("port", default=8888, type=int, help="运行端口")


class CustomApplication(tornado.web.Application):
    def __init__(self):
        """重写__init__"""
        handlers = urls
        settings = configs
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


class Create_Server():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        CustomApplication()
    )
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
