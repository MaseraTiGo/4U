# -*- coding: utf-8 -*-
# @File    : st_profile
# @Project : x_web
# @Time    : 2023/9/13 11:41
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import json

import altair as alt
import pandas as pd
import requests
import streamlit as st
from streamlit_echarts import st_echarts

from super_dong.gui import ip, headers

# import atexit
# import os
#
# import django
# import streamlit as st
#
# from const import fucking_prefix
# from super_dong.frame.utils.redis import redis_sys
#
# # Set page title
# st.set_page_config(page_title="Affiliate Management App")
#
#
# # Define Streamlit app
# def init_django():
#     init_flag = redis_sys.get('init_django')
#     if init_flag:
#         return
#     print(f"{fucking_prefix} init django start...")
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
#     django.setup()
#     print(f"{fucking_prefix} init django over.")
#     redis_sys.set('init_django', 'fuck-you')
#
#
# def clear_redis():
#     redis_sys.delete('init_django')
#     print("init_django key deleted from Redis.")
#
#
# # Register function to clear Redis on exit
# atexit.register(clear_redis)
#
# # Run Streamlit app
# if __name__ == "__main__":
#     init_django()

df = None
new_data = None


def get_profile_data():
    profile_url = f"http://{ip}/apis/admin/money/shitprofile"

    response_data = requests.post(profile_url, data=json.dumps({}),
                                  headers=headers)
    return response_data.json()


def show_total_table():
    global df, new_data
    data = get_profile_data()['data']['data']['profile']

    new_data = []
    for key, value in data.items():
        value['date'] = key
        new_data.append(value)

    df = pd.DataFrame(new_data)
    # Number of items to display per page
    items_per_page = st.slider("Number of items per page", min_value=1,
                               max_value=len(df), value=5)

    # Page selection
    page = st.number_input("Select Page", min_value=1,
                           max_value=(len(df) // items_per_page) + 1)

    # Display the data in a table for the selected page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(df))

    st.write("Data:")

    styled_df = df.iloc[start_idx:end_idx].style.format(
        {
            "Total": '{:.2f}',
            "Net_worth": '{:.2f}',
        }
    )
    st.write(styled_df, unsafe_allow_html=True)
    return start_idx, end_idx


def show_charts(start_idx, end_idx):
    st.write("Total Trending:")

    re_data = list(reversed(new_data[start_idx: end_idx]))
    dates = [item['date'] for item in re_data]
    totals = [item['Total'] for item in re_data]
    net_worths = [item['Net_worth'] for item in re_data if
                  item['Net_worth'] < 1000]

    yAxis_start_total = 600_000
    # yAxis_start_net_worth = 0

    total_chart = {
        "xAxis": {"type": "category", "data": dates},
        "yAxis": {"type": "value", "min": yAxis_start_total, "interval": 20000},
        # Set the desired start value here
        "tooltip": {"trigger": "axis", "formatter": "{b}: {c}"},
        "series": [{"data": totals, "type": "line", "name": "Total"}],
    }
    st_echarts(options=total_chart, key="total_chart")

    net_worth_chart = {
        "xAxis": {"type": "category", "data": dates},
        "yAxis": {"type": "value", "interval": 200},
        # Set the desired start value here
        "tooltip": {"trigger": "axis", "formatter": "{b}: {c}"},
        "series": [{"data": net_worths, "type": "line", "name": "Net Worth"}],
    }
    st_echarts(options=net_worth_chart, key="net_worth_chart")


def old_chat(start_idx, end_idx):
    chart = alt.Chart(df.iloc[start_idx:end_idx]).mark_line().encode(
        x='date',
        y='Total'
    ).properties(
        width=900,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

    st.write("Networth Trending:")
    chart = alt.Chart(df.iloc[start_idx:end_idx]).mark_line().encode(
        x='date',
        y='Net_worth'
    ).properties(
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)


def run():
    show_charts(*show_total_table())
