from __future__ import absolute_import
from . import app


# from celery.schedules import crontab


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, hello.s(), name='test hello every 5')
    sender.add_periodic_task(10, fuck.s('10s, past'), expires=10)


@app.task
def hello():
    print('hello welcome')


@app.task
def fuck(string):
    print(string.upper())
