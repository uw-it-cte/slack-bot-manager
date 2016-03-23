from django.utils.log import getLogger
from django.db import connection
from manager.models import SlackBot
from multiprocessing import Process


class SlackBotManager(object):

    def __init__(self, api_token):
        self._api_token = api_token
        self._log = getLogger(__name__)

    def launch(self, launcher):
        # background the bot
        self._log.info('Starting %s' % (self.name))
        connection.close()
        p = Process(target=self.bot)
        p.start()

        bot = SlackBot(pid=p.pid,name=self.name,
                       description=self.description,started_by=launcher)
        bot.save()
        return bot.pk
