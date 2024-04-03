"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import re_path, path

from super_dong.frame.core.api_doc.views import api_doc
from super_dong.frame.router import executor
from super_dong.views import index, adminer, shit_trend_line
from django.views.generic import RedirectView

re_pattern = f'{settings.API_ROUTER_PREFIX}/.+'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path("adminer-mysql.php", RedirectView.as_view(url='adminer-mysql.php', permanent=False)),
    path('', index, name='index'),
    path('line', shit_trend_line, name='line'),
    re_path(re_pattern, executor),
    re_path("api_doc", api_doc)
]
