from tornado import web
import tornado


class MainHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("hello world")


if __name__ == '__main__':
    app = web.Application([('/', MainHandler)])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
