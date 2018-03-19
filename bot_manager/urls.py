from django.conf.urls import url, include
from bot_manager.views.bots import BotView, BotListView


urlpatterns = [
    url(r'api/v1/bot/(?P<bot_id>[0-9]+)?$', BotView().run),
    url(r'api/v1/bots/?$', BotListView().run),
]
