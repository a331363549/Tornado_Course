from sockjs.tornado import SockJSRouter  # 定义路由
from apps.views.index import IndexHandler
from apps.views.real_time import ReaTimeHandler as real_time

urls = [
           (r"/", IndexHandler)
] + SockJSRouter(real_time, "/real_time/").urls
