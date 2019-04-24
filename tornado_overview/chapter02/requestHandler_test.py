from tornado.web import RequestHandler
from tornado import web
import tornado


class MainHandler(RequestHandler):

    # 用户初始化
    def _initialize(self):
        pass

    # 用户真正调用请求处理之前的初始化方法
    def prepare(self):
        pass

    # 关闭句柄 清理内存
    def on_finish(self):
        pass

    # http方法
    def get(self):
        """
        只用于get方法
        self.get_query_argument()    返回最后一个name参数
        self.get_query_arguments()   返回一个list
        """
        data1 = self.get_query_argument("name")
        data2 = self.get_query_arguments("name")
        pass

    def post(self):
        """
        self.request.arguments()  获取所有参数

        post get 方法都能使用
        self.get_argument()     返回最后一个name参数
        self.get_arguments()    返回一个list

         需要现将请求参数头部进行设置  见request_test.py中的示例
        self.get_body_argument()    返回body中的参数
        self.get_body_arguments()
        """
        # data = self.request.arguments()
        data1 = self.get_argument("name")
        data2 = self.get_arguments("name")
        data3 = self.get_body_argument("name")
        data4 = self.get_body_arguments("name")
        pass

    def delete(self):
        pass

    def patch(self):
        pass

    # 输出
    """
    self.set_status()   设置状态码
    self.write()        返回消息
    self.finish()       结束
    self.redirect()     跳转到指定链接
    self.write_error()  定义错误跳转页面
    """


urls = [
    ('/', MainHandler),
]

if __name__ == '__main__':
    app = web.Application(urls)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
