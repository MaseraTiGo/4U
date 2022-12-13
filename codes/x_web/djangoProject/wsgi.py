"""
WSGI config for djangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

from djangoProject import FRAME_PREFIX

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = get_wsgi_application()

# --------------- migrate the migrations 2 db ---------------
from django.core import management


def migrate_my_models():
    dbs = settings.DATABASE_APPS_MAPPING.items()
    for app, db in dbs:
        management.call_command("migrate", app, database=db)
        print(f"{FRAME_PREFIX} {db} migrate successfully!\n")


migrate_my_models()
# --------------- migrate the migrations 2 db ---------------

# =============== command need to be executed before app starts ================

print(f"{FRAME_PREFIX} now, fucking hit me!")
