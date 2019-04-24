from tornado import web
from tornado.options import define, options, parse_command_line
import tornado

# define 定义一些在命令行中传递参数以及类型
define("port", default=8008, help="run on the given port", type=int)
define("debug", default=True, help="set tornado debug mode", type=bool)

# 执行命令行
# options.parse_command_line()
# 读取配置文件
options.parse_config_file("conf.cfg")


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
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()