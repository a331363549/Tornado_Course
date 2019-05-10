from sockjs.tornado import SockJSConnection


class ReaTimeHandler(SockJSConnection):
    waiters = set()

    def on_open(self, request):
        """打开连接"""
        try:
            self.waiters.add(self)
        except Exception as e:
            print(e)

    def on_message(self, message):
        """发送消息"""
        try:
            self.broadcast(self.waiters,message)
        except Exception as e:
            print(e)

    def on_close(self):
        """关闭链接"""
        try:
            self.waiters.remove(self)
        except Exception as e:
            print(e)
