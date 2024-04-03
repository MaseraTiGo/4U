"""
WSGI config for djangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from autorun.auto_detect_dollar import dollar_run
from djangoProject import FRAME_PREFIX
from super_dong.frame.contri.wechat import auto_quick_create

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = get_wsgi_application()

# =============== command need to be executed before app starts ================

# =============== command need to be executed before app starts ================
from threading import Thread
Thread(target=auto_quick_create).start()
Thread(target=dollar_run).start()
print(f"{FRAME_PREFIX} now, fucking hit me!")
