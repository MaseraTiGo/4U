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
import atexit
import os

import django
import streamlit as st

from const import fucking_prefix
from super_dong.frame.utils.redis import redis_sys

# Set page title
st.set_page_config(page_title="Affiliate Management App")


# Define Streamlit app
def app():
    # Set app title
    st.title("Affiliate Management System")

    # Define sidebar options
    # options = ["Affiliate", "Affiliate Account"]
    options = ModelRepo.get_options()
    choice_model = st.sidebar.selectbox("Select Model", options)

    operations = [f"{op}_{choice_model}" for op in OPERATION]
    choice_op = st.sidebar.selectbox("Select operation", operations)
    ModelRepo.execute(choice_model, choice_op)


def init_django():
    init_flag = redis_sys.get('init_django')
    if init_flag:
        return
    print(f"{fucking_prefix} init django start...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
    django.setup()
    print(f"{fucking_prefix} init django over.")
    redis_sys.set('init_django', 'fuck-you')


def clear_redis():
    redis_sys.delete('init_django')
    print("init_django key deleted from Redis.")


# Register function to clear Redis on exit
atexit.register(clear_redis)

# Run Streamlit app
if __name__ == "__main__":
    init_django()

    from st_md.base_md import ModelRepo, OPERATION

    app()
