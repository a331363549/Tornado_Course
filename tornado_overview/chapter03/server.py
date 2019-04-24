from tornado import web
import tornado
from tornado.web import template,StaticFileHandler


class MainHandler(web.RequestHandler):
    def get(self):
        self.render("message.html")


settings = {
    "static_path": "/home/ding/桌面/github/Tornado_Course/tornado_overview/chapter03/static",
    "static_url_prefix": "/static/",  # 开启后上面的静态路径被替换成此处命名的路径,
    "template_path": "templates",
}

if __name__ == '__main__':
    app = web.Application([
        ('/', MainHandler),
    ], **settings,
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
