from tornado import web
import tornado
from aiomysql import create_pool
from tornado import gen, httpclient, ioloop


class MainHandler(web.RequestHandler):
    def initialize(self, db):
        self.db = db

    async def get(self):
        id = ''
        name = ''
        email = ''
        address = ''
        message = ''
        async with create_pool(host=self.db['host'], port=self.db['port'],
                               user=self.db['user'], password=self.db['password'],
                               db=self.db['name'], charset="utf8") as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT id,name,email,address,message from message")
                    id, name, email, address, message = await cur.fetchone()
                    # print(value)
        self.render("message.html", id=id, name=name, email=email, address=address, message=message)

    async def post(self):
        id = self.get_body_argument("id", "")
        name = self.get_body_argument("name", "")
        email = self.get_body_argument("email", "")
        address = self.get_body_argument("address", "")
        message = self.get_body_argument("message", "")
        async with create_pool(host=self.db['host'], port=self.db['port'],
                               user=self.db['user'], password=self.db['password'],
                               db=self.db['name'], charset="utf8") as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    if not id:
                        await cur.execute(
                            "INSERT INTO message(name,email,address,message) VALUES('{}','{}','{}','{}')".format(name,
                                                                                                                 email,
                                                                                                                 address,
                                                                                                                 message))
                    else:
                        await cur.execute(
                            "update message set name='{}', email='{}',address='{}',message='{}'".format(name, email,
                                                                                                        address,
                                                                                                        message))
                    await conn.commit()
        self.render("message.html", id=id, name=name, email=email, address=address, message=message)


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
