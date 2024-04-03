# -*- coding: utf-8 -*-
# @File    : simple_line_chart
# @Project : x_web
# @Time    : 2024/4/3 10:31
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from datetime import datetime

from bokeh.models import SingleIntervalTicker, BasicTickFormatter, HoverTool, AdaptiveTicker
from bokeh.plotting import figure, output_file, save


def gen_html(days):
    # from super_dong.model_store.models import MyShit
    from super_dong.apis.admin.money.manager import MyShitManager

    date_mapping_amount = MyShitManager.shit_profile()
    dates = [datetime.strptime(cur_day, '%Y-%m-%d') for cur_day in
             date_mapping_amount.keys()][:days]
    amount = [i['Total'] for i in date_mapping_amount.values()][:days]
    min_ = min(dates)
    max_ = max(amount)

    hover_tool = HoverTool()
    hover_tool.formatters = {
        "@x": "datetime",
        "@y": "numeral"
    }
    hover_tool.tooltips = [
        ("X", "@x{%F}"),  # Format X with ISO 8601 date format (YYYY-MM-DD)
        ("Y", "@y{0,0}")  # Format Y as integer with thousand separators
    ]

    # create a new plot with a title and axis labels
    p = figure(title="My Finance Trends", x_axis_label="Date",
               x_axis_type="datetime", sizing_mode="stretch_width",
               y_axis_label="Amount",
               )

    p.scatter(dates, amount, size=8)
    p.line(dates, amount, legend_label="Amount", line_width=2)
    p.toolbar.logo = None
    p.tools.append(hover_tool)

    def set_y():
        # p.y_range.start = min_
        # p.y_range.end = max_
        # p.yaxis.ticker = SingleIntervalTicker(interval=int((max_ - min_) / 10))
        p.yaxis.ticker = AdaptiveTicker()
        p.yaxis.formatter = BasicTickFormatter(use_scientific=False)
        p.ygrid.band_fill_color = "olive"
        p.ygrid.band_fill_alpha = 0.15

    set_y()

    output_file("./templates/bokeh_ui/lines/my_line.html",
                mode="inline")

    save(p)
