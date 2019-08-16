# -*- coding: utf-8 -*-
# file_name       : signal001.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 8/13/2019 8:26 AM
from django.dispatch.dispatcher import receiver, Signal

# shut_down_alarm = Signal(providing_args=('shutting down', 'shut_down_alarm'))

print('test--------------->')
shut_down_alarm = Signal(providing_args=('shutting down', 'shut_down_alarm'))


@receiver(shut_down_alarm, sender='fucker')
def call_back(sender, *args, **kwargs):
    print('shutting ===========>')
    print(args)
    print(kwargs)


shut_down_alarm.send(sender='fucker', **{'hello': 'world'})
shut_down_alarm.disconnect(receiver=call_back, sender='fucker')
shut_down_alarm.send(sender='fucker', **{'hello': 'world'})
