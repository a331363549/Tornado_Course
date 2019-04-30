from tornado import web
import tornado
from aiomysql import create_pool
from tornado import gen, httpclient, ioloop
from chapter05.forms import MessageForm
from chapter05.models import Message


class MainHandler(web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self):
        message_form = MessageForm()
        self.render("message.html", message_form=message_form)

    async def post(self):
        message_form = MessageForm(self.request.arguments)
        if message_form.validate():
            # 验证通过,获取值并保存
            name = message_form.name.data
            email = message_form.email.data
            address = message_form.address.data
            msg = message_form.message.data

            message =  Message()
            message.name = name
            message.email = email
            message.address = address
            message.message = msg
            message.save()

            self.render("message.html", message_form=message_form)
        else:

            self.render("message.html", message_form=message_form)


settings = {
    "static_path": "/home/ding/桌面/github/Tornado_Course/tornado_overview/chapter03/static",
    "static_url_prefix": "/static/",  # 开启后上面的静态路径被替换成此处命名的路径,
    "template_path": "templates",
    'db': {
        "host": "127.0.0.1",
        "user": "root",
        "password": "123",
        "name": "message",
        "port": 3306
    }
}

if __name__ == '__main__':
    app = web.Application([
        ('/', MainHandler, {'db': settings['db']}),
    ], **settings,
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
