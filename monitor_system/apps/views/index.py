import tornado.web
from apps.tools.monitor import Monitor
from apps.tools.chart import Chart


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        m = Monitor()
        c = Chart()
        cpu_info = m.cpu()
        print(cpu_info)
        self.render("index.html")
