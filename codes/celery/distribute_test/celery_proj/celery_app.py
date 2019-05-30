from __future__ import absolute_import
from celery import Celery
# import os
# import json

app = Celery('celery_app')
app.config_from_object('celery_config')
# os.environ.update({'celery_app': json.dumps(app)})
