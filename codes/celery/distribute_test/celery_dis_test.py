# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '5/29/2019 6:00 PM'

from __future__ import absolute_import
from celery import Celery

app = Celery('celery_dis_test', backend='redis://192.168.199.209', broker='amqp://aston:123918@192.168.199.209//')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, say_fuck.s('i love you'), name='every 5 sec')


@app.task
def say_fuck(string):
    return string.upper()


if __name__ == '__main__':
    app.start()
