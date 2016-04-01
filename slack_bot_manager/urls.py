from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'bot_manager.views.home.home', name='home'),
    url(r'^botmgr/', include('bot_manager.urls')),
)
