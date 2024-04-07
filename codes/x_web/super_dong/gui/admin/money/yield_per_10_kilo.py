# -*- coding: utf-8 -*-
# @File    : yield_per_10_kilo
# @Project : x_web
# @Time    : 2024/4/3 15:01
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import pandas as pd
from bokeh.io import output_file, save
from bokeh.models import HoverTool, AdaptiveTicker
from bokeh.plotting import figure
from bokeh.transform import dodge


def gen_html():
    from super_dong.apis.admin.money.manager import MyShitManager
    data = MyShitManager.ten_grand_share({"show_num": 30, "invest_level": 5})

    # Extract keys and average_net_worth values
    keys = list(data.keys())
    average_net_worth_values = [entry['average_net_worth'] for entry in
                                data.values()]

    # Create a DataFrame for easier plotting
    df = pd.DataFrame(
        {
            'keys': keys,
            'average_net_worth': average_net_worth_values
        }
    )

    # # Define the range of the y-axis
    # y_range = (
    #     min(df['average_net_worth']) * 0.9,
    #     max(df['average_net_worth']) * 1.1
    # )

    # Create Bokeh figure with defined y-axis range
    p = figure(
        x_range=keys,
        title="Average Net Worth by Investment",
        sizing_mode="stretch_width",
    )

    # Add vbar glyphs for each key
    bars = p.vbar(x=dodge('keys', 0, range=p.x_range), top='average_net_worth',
                  width=0.4, source=df, color="green")

    # Configure hover tool to display relevant data
    hover = HoverTool(tooltips=[
        # ("Key", "@keys"),
        ("Average Net Worth", "@average_net_worth")
    ],
        renderers=[bars])
    p.add_tools(hover)

    # Configure plot
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1.2

    p.yaxis.ticker = AdaptiveTicker()

    # Add text labels for the values
    p.text(
        x='keys', y='average_net_worth', text='average_net_worth',
        text_align='center', text_baseline='top', source=df,
        y_offset=-13,
    )

    output_file("./templates/bokeh_ui/lines/my_histogram.html",
                mode="inline")
    save(p)
