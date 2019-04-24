from tornado import web
import tornado


class MainHandler(web.RequestHandler):
    async def get(self):
        self.write("hello world")


class MainHandler2(web.RequestHandler):
    async def get(self):
        self.write("1233")


class PeopleIdHandler(web.RequestHandler):
    async def get(self, id):
        self.write("用户id={}".format(id))


class PeopleNameHandler(web.RequestHandler):
    async def get(self, name):
        self.write("用户姓名={}".format(name))


class PeopleInfoHandler(web.RequestHandler):
    async def get(self, name, age, gender):
        self.write("用户姓名={}, 用户年龄={}, 用户性别={}".format(name, age, gender))


urls = [
    ('/', MainHandler),
    ('/test/?', MainHandler2),
    ('/people/(\d+)/?', PeopleIdHandler),
    ('/people/(\w+)/?', PeopleNameHandler),
    tornado.web.URLSpec("/people/(?P<name>\w+)/(?P<age>\d+)/(?P<gender>\w+)/?", PeopleInfoHandler)
]

if __name__ == '__main__':
    app = web.Application(urls)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# self.write() 页面返回消息
# self.redirect("url","args")  跳转url

# url命名
# tornado.web.URLSpec()

# tornado.web.URLSpec("/people/(?P<name>\w+)/(?P<age>\d+)/(?P<gender>\w+)/?")
# self.write("用户姓名={}, 用户年龄={}, 用户性别={}".format(name,age,gender))
# 此处的参数名称与链接中传入的参数名称应该一致 增强代码可读性
