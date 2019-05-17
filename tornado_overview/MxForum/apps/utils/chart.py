# -*- coding: utf-8 -*-
import datetime
from pyecharts.charts import Liquid, Gauge, Pie, Line
from pyecharts import options as opts


class Chart(object):
    # 水球图
    def liquid_html(self, chart_id, title, val):
        # 基本配置
        liquid = (
            Liquid()
                .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                           title_textstyle_opts={
                                                               "color": "white",
                                                               "fontWeight": 20,
                                                               "fontSize": 14,
                                                               "lineHeight": 50,
                                                           }
                                                           ))
        )

        # 绑定id
        liquid.chart_id = chart_id
        # 添加参数
        liquid.add("", [round(val / 100, 4)])
        return liquid.render_embed()  # 返回图表html代码

    # 仪表图
    def gauge_html(self, chart_id, title, val):
        gauge = (
            Gauge()
                .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                           title_textstyle_opts={
                                                               "color": "white",
                                                               "fontWeight": 200,
                                                               "fontSize": 20,
                                                               "lineHeight": 200,
                                                           }
                                                           ))
                .add("", [("使用率", val)])
        )
        gauge.chart_id = chart_id
        # gauge.add(
        #     "",
        #     "",
        #     val,
        #     # scale_range=[0, 100],
        #     # is_legend_show=False
        # )
        return gauge.render_embed()

    # 饼状图
    def pie_two_html(self, chart_id, title, sub_title1, sub_title2, key1, key2, val1, val2):
        # 实例化饼状图
        pie = (
            Pie()
                .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                           title_textstyle_opts={
                                                               "color": "white",
                                                               "fontWeight": 300,
                                                               "fontSize": 14,
                                                               "lineHeight": 300,
                                                           }
                                                           ))

                # 绑定属性和值
                .add(
                sub_title1,
                [list(z) for z in zip(key1, val1)],
                center=["25%", "50%"],
                radius=["30%", "75%"],
                rosetype="area",
                label_opts=opts.LabelOpts(color="white"),
                # itemstyle_opts=opts.ItemStyleOpts(c="red"),

            )
                .add(
                sub_title2,
                [list(z) for z in zip(key2, val2)],
                radius=["30%", "75%"],
                center=["25%", "50%"],
                rosetype="area",
            )
        )
        # 指定ID
        pie.chart_id = chart_id

        return pie.render_embed()

    # 折线面积图
    def line_html(self, title, key, val, color=None):
        line = (
            Line()
                .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                           title_textstyle_opts={
                                                               "color": "white",
                                                               "fontWeight": 300,
                                                               "fontSize": 14,
                                                               "lineHeight": 300,
                                                           }
                                                           ))
                .add_xaxis(key)
                .add_yaxis(title, val)
            # [list(z) for z in zip(key, val)],

            # mark_point=["average", "max", "min"],
            # mark_line=["average", "max", "min"],
            # area_color=color,
            # line_opacity=0.2,
            # area_opacity=0.4,
            # is_datazoom_show=True,
            # datazoom_range=[0, 100],
            # symbol=None
        )
        return line.render_embed()

    # 折线面积图
    def line_three_html(self, title, key, val_min, val_max, val_avg):
        # line = Line(
        #     title,
        #     title_pos="left",
        #     width="100%",
        #     height=300
        # )
        line = (
            Line()
                .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                           title_textstyle_opts={
                                                               "color": "white",
                                                               "fontWeight": 300,
                                                               "fontSize": 14,
                                                               "lineHeight": 300,
                                                           }
                                                           ))
        )
        # line.add(
        #     "最小值",
        #     key,
        #     val_min,
        #     # mark_point=["average", "max", "min"],
        #     # is_datazoom_show=True,
        #     # datazoom_range=[0, 100],
        #     # is_smooth=True
        # )
        # line.add(
        #     "最大值",
        #     key,
        #     val_max,
        #     # mark_point=["average", "max", "min"],
        #     # is_datazoom_show=True,
        #     # datazoom_range=[0, 100],
        #     # is_smooth=True
        # )
        # line.add(
        #     "平均值",
        #     key,
        #     val_avg,
        #     # mark_point=["average", "max", "min"],
        #     # is_datazoom_show=True,
        #     # datazoom_range=[0, 100],
        #     # is_smooth=True
        # )
        return line.render_embed()

    # 日期时间方法
    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
