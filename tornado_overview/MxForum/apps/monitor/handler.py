import json
import uuid

from MxForum.MxForm.handler import RedisHandler, CommonHandler
import os
from playhouse.shortcuts import model_to_dict
from MxForum.apps.utils.util_func import json_serial
from MxForum.apps.utils.monitor import Monitor
from MxForum.apps.utils.chart import Chart
from sockjs.tornado import SockJSConnection
import tornado.gen
import tornado.concurrent


class SystemInfoHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        m = Monitor()
        c = Chart()
        cpu_info = m.cpu()
        mem_info = m.mem()
        swap_info = m.swap()
        net_info = m.net()
        disk_info = m.disk()
        net_pie = [
            c.pie_two_html(
                "net{}".format(k + 1),
                "{}网卡信息".format(v["name"]),
                "收发包数统计",
                "收发字节统计",
                ["收包数", "发包数"],
                ["收字节", "发字节"],
                [v["packets_recv"], v["packets_sent"]],
                [v["bytes_recv"], v["bytes_sent"]],
            )
            for k, v in enumerate(net_info) if v["packets_recv"] and v['packets_sent']
        ]
        self.html("index.html",
                  data=dict(
                      title="系统监控",
                      cpu_info=cpu_info,
                      mem_info=mem_info,
                      swap_info=swap_info,
                      net_info=net_info,
                      disk_info=disk_info,
                      cpu_liquid=c.liquid_html("cpu_avg", "CPU平均使用率", cpu_info['percent_avg']),
                      mem_gauge=c.gauge_html("mem", "内存使用率", mem_info['percent']),
                      swap_gauge=c.gauge_html("swap", "交换分区使用率", swap_info['percent']),
                      net_pie=net_pie,
                  )
                  )


class LogHandler(RedisHandler):
    async def post(self):
        pass


class RealTimeHandler(SockJSConnection):
    # 定义一个连接池，所有客户端的一个集合
    waiters = set()  # 集合元素不重复的对象

    # 1.建立连接
    def on_open(self, request):
        try:
            self.waiters.add(self)
        except Exception as e:
            print(e)

    # 2.发送消息
    def on_message(self, message):
        try:
            m = Monitor()
            data = dict()
            if message == "system":
                data = dict(
                    mem=m.mem(),
                    swap=m.swap(),
                    cpu=m.cpu(),
                    disk=m.disk(),
                    net=m.net(),
                    dt=m.dt()
                )
            # 对消息进行处理，把新的消息推送到所有连接的客户端
            self.broadcast(self.waiters, json.dumps(data))  # 广播
        except Exception as e:
            print(e)

    # 3.关闭连接
    def on_close(self):
        try:
            self.waiters.remove(self)
        except Exception as e:
            pass
