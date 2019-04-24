# StaticFileHandler     处理静态文件
# static_url_prefix  可将链接的目录重命名

# RedirectHandler       处理重定向
# 301 永久重定向
# 302 临时重定向
# self.redirect 方法和 RedirectHandler区别
# RedirectHandler 永久性的定向
# self.redirect 可实现自己的逻辑  实用性更强


from tornado import web
import tornado
from tornado.web import StaticFileHandler, RedirectHandler


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("hello world")


class MainHandler2(web.RequestHandler):
    def get(self):
        self.write("hello hello")


settings = {
    "static_path": "/home/ding/PycharmProjects/tornado_overview/chapter02/static",
    "static_url_prefix": "/static2/," #开启后上面的静态路径被替换成此处命名的路径
}

if __name__ == '__main__':
    app = web.Application([
        ('/', MainHandler),
        ("/2/?", RedirectHandler, {"url": "/"}),
        ("/static3/(.*)", StaticFileHandler, {"path": "/home/ding/PycharmProjects/tornado_overview/chapter02/static"}),
    ], **settings
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
