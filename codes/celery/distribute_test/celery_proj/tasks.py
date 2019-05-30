from __future__ import absolute_import
# import os
# import json
# import sys
#
# sys.path.append(os.path.abspath(__file__))

from celery_app import app


# app = json.loads(os.environ.get('celery_app', Ellipsis))


@app.task
def add(x, y):
    return x + y


@app.task
def say(string):
    string = str(string)
    return string.upper()
