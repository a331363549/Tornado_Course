import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options
from tornado.web import RequestHandler
import torndb
import redis

import config
from urls import handlers

define("port", type=int, default=8000, help="run server on the given port")


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = torndb.Connection(**config.mysql_option)
        self.redis = redis.StrictRedis(**config.redis_option)
        # self.db = torndb.Connection(
        #     host=config.mysql_option["host"],
        #     database=config.mysql_option["ihome"],
        #     user=config.mysql_option["root"],
        #     password=config.mysql_option["password"],
        # )
        # self.redis = redis.StrictRedis(
        #     host=config.mysql_option["host"],
        #     port=config.mysql_option["port"],
        # )


def main():
    # options.logging = config.log_lever
    # options.log_file_prefix = config.log_file
    tornado.options.parse_command_line()
    app = Application(
        handlers, **config.settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # http_server.bind(8000)
    # http_server.start(0)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
