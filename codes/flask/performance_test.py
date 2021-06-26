# -*- coding: utf-8 -*-

# ===================================
# file_name     : performance_test.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2021/6/7 21:43
# ide_name      : PyCharm
# project_name  : flask
# ===================================

"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""

from memory_profiler import profile


@profile
def start_flask():
    from flask_primary import app
    with app.app_context():
        print(f"dong ---------------> gonna do something.")


start_flask()
