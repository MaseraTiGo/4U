from kombu import Exchange
from kombu import Queue
from datetime import timedelta

result_serializer = 'json'

broker_url = 'amqp://aston:123918@192.168.1.134:5672//'
result_backend = 'redis://192.168.1.134'

timezone = 'Asia/shanghai'

imports = ('tasks',)

# beat_schedule = {
#     'add-every-3-sec': {
#         'task': 'tasks.add',
#         'schedule': 3,
#         'args': (30, 3)
#     },
#     'upper-every-6-sec': {
#         'task': 'tasks.say',
#         'schedule': timedelta(seconds=6),
#         'args': (3)
#     }
# }

task_queues = (
    Queue('default', exchange=Exchange('default'), routing_key='default'),
    Queue('priority_high', exchange=Exchange('priority_high'), routing_key='priority_high'),
    Queue('priority_low', exchange=Exchange('priority_low'), routing_key='priority_low')
)

task_routes = {
    'tasks.add': {'queue': 'priority_low', 'routing_key': 'priority_low'},
    'tasks.say': {'queue': 'priority_high', 'routing_key': 'priority_high'}
}
