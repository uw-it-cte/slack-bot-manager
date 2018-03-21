from django.conf.urls import include, url
from django.contrib import admin

from bot_manager.views import home

urlpatterns = [
    url(r'^$', home.home, name='home'),
    url(r'^botmgr/', include('bot_manager.urls')),
]
