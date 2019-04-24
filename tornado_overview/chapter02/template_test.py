from tornado import web
import tornado
from tornado.web import template


# template 模板

class MainHandler(web.RequestHandler):
    def get(self):
        word = "hello"
        self.render("hello.html", word=word)
        # loader = template.Loader("/home/ding/PycharmProjects/tornado_overview/chapter02/static/templates")
        # self.finish(loader.load("hello.html").generate(wrod=word))


class MainHandler2(web.RequestHandler):
    def get(self):
        self.write("hello hello")


settings = {
    "static_path": "/home/ding/PycharmProjects/tornado_overview/chapter02/static",
    # "static_url_prefix": "/static2/,"  # 开启后上面的静态路径被替换成此处命名的路径,
    "template_path": "static/templates",
}

if __name__ == '__main__':
    app = web.Application([
        ('/', MainHandler),
    ], **settings
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
