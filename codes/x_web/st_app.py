# -*- coding: utf-8 -*-
# @File    : st_app
# @Project : x_web
# @Time    : 2023/7/12 16:56
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""

import streamlit as st

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


# Streamlit app
st.title("Finance Data Visualization")


class Menu:
    Profile = 'Profile'
    Tab2 = 'tab2'
    Tab3 = 'tab3'


current_menu = st.radio("=" * 88, [Menu.Profile, Menu.Tab2, Menu.Tab3],
                        horizontal=True)

if current_menu == Menu.Profile:
    from super_dong.gui.admin.money.st_profile import run

    run()

print(f"dong ----------------------> fuck all of you!!!")
