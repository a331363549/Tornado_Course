import datetime
from pyecharts.charts import Liquid
# from pyecharts


"""
参考连接： pyecharts.org
"""

class Chart(object):
    """水球图"""

    def liquid_html(self, chart_id, title, val):
        liquid = Liquid(
            "{}--{}".format(
                self.dt, title
            ),
            title_pos="center",
            width="100%",
            title_color="white",
            title_text_size=14,
            height=300
        )
        liquid.chart_id = chart_id
        liquid.add("", [round(val / 100, 4)])
        return liquid.render_embed()

    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
