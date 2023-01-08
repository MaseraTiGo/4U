"""
WSGI config for djangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from djangoProject import FRAME_PREFIX

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = get_wsgi_application()

# =============== command need to be executed before app starts ================

# =============== command need to be executed before app starts ================

print(f"{FRAME_PREFIX} now, fucking hit me!")
