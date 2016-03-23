from django.conf.urls import patterns, url, include
from manager.views.bots import BotView, BotListView


urlpatterns = patterns(
    '',
    url(r'api/v1/bot/(?P<bot_id>[0-9]+)?$', BotView().run),
    url(r'api/v1/bots/?$', BotListView().run),
)
