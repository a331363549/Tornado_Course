from tornado import web
import tornado
from tornado.web import template


# template 模板

class MainHandler(web.RequestHandler):
    def get(self):
        # word = "hello"
        orders = [
            {
                "name": "小米T恤 忍者米兔双截棍 军绿 XXL",
                "image": "http://i1.mifile.cn/a1/T11lLgB5YT1RXrhCrK!40x40.jpg",
                "price": 39,
                "nums": 3,
                "detail": "<a href='http://www.baidu.com'>查看详情</a>"
            },
            {
                "name": "招财猫米兔 白色",
                "image": "http://i1.mifile.cn/a1/T14BLvBKJT1RXrhCrK!40x40.jpg",
                "price": 49,
                "nums": 2,
                "detail": "<a href='http://www.baidu.com'>查看详情</a>"
            },
            {
                "name": "小米圆领纯色T恤 男款 红色 XXL",
                "image": "http://i1.mifile.cn/a1/T1rrDgB4DT1RXrhCrK!40x40.jpg",
                "price": 59,
                "nums": 1,
                "detail": "<a href='http://www.baidu.com'>查看详情</a>"
            }
        ]
        self.render("index.html", orders=orders)
        # loader = template.Loader("/home/ding/PycharmProjects/tornado_overview/chapter02/static/templates")
        # self.finish(loader.load("hello.html").generate(wrod=word))


class MainHandler2(web.RequestHandler):
    def get(self):
        self.write("hello hello")


settings = {
    "static_path": "/home/ding/桌面/github/Tornado_Course/tornado_overview/chapter02/static",
    # "static_url_prefix": "/static2/,"  # 开启后上面的静态路径被替换成此处命名的路径,
    "template_path": "templates",
}

if __name__ == '__main__':
    app = web.Application([
        ('/', MainHandler),
    ], **settings,
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
