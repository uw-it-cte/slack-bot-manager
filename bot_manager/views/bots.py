from django.conf import settings
from django.apps import apps
from django.db.utils import OperationalError
from django.middleware.csrf import get_token
from django.db import connection
from bot_manager.models import Bot
from bot_manager.slackbot import SlackBot
from bot_manager.views import RESTDispatch
from multiprocessing import Process, get_logger
from logging import getLogger
from importlib import import_module
import imp
import json
import inspect
import os
import psutil
import signal



def bot_is_active(pid):
    return psutil.pid_exists(pid) if pid > 0 else False


def run_slackbot(bot_class):
    bot_class(logger=get_logger()).bot()


class BotView(RESTDispatch):
    """ Retrieves a Bot model.
        GET returns 200 with Bot details.
        PUT returns 200.
    """
    def __init__(self):
        self._log = getLogger(__name__)

    def GET(self, request, **kwargs):
        bot_id = kwargs['bot_id']
        try:
            bot = Bot.objects.get(id=bot_id)
            bot.is_active = bot_is_active(bot.pid)
            bot.csrf_token = get_token(request)
            return self.json_response(json.dumps(bot.json_data()))
        except Bot.DoesNotExist:
            return self.json_response(
                '{"error":"bot %s not found"}' % bot_id, status=404)

    def PUT(self, request, **kwargs):
        bot_id = kwargs['bot_id']
        try:
            bot = Bot.objects.get(id=bot_id)
            bot.is_active = bot_is_active(bot.pid)
            data = json.loads(request.body).get('bot', {})
            if 'is_active' in data:
                if data['is_active']:
                    if not bot.is_active:
                        ### start bot
                        bot_module = import_module(bot.module_name)
                        bot_class = getattr(bot_module, bot.class_name)
                        bot.pid = self._launch(bot_class)
                        bot.is_active = True

#                        bot.changed_by = request.user.username
#                        bot.changed_date = datetime.utcnow().replace(tzinfo=utc)
                        bot.save()
                        self._log.info('%s started Bot "%s"' % (
                            bot.changed_by, bot.class_name))
                elif bot.is_active:
                    ### stop bot
                    if self._kill(bot.pid):
                        bot.is_active = False
                        bot.pid = 0
                        bot.save()
                        self._log.info('%s stopped Bot "%s"' % (
                            bot.changed_by, bot.class_name))
                    else:
                        return self.json_response(
                            '{"error":"cannot stop bot %s"}' % bot_id, status=500)
            return self.json_response(json.dumps({'bot': bot.json_data()}))
        except Bot.DoesNotExist:
            return self.json_response(
                '{"error":"bot %s not found"}' % bot_id, status=404)

    def _launch(self, bot_class):
        # background the bot
        connection.close()
        p = Process(target=run_slackbot, args=(bot_class,))
        p.start()
        return p.pid

    def _kill(self, pid):
        if pid > 0:
            try:
                os.kill(pid, signal.SIGKILL)
                os.waitpid(pid, 0)
            except OSError:
                return False

        return True


class BotListView(RESTDispatch):
    """ Retrieves a list of Bots.
    """
    def GET(self, request, **kwargs):
        try:
            self._reconcile_bots()
        except OperationalError:
            pass

        bots = []
        for bot in Bot.objects.all().order_by('class_name'):
            bot.is_active = bot_is_active(bot.pid)
            bots.append(bot.json_data())

        return self.json_response(json.dumps({'bots': bots}))

    def _reconcile_bots(self):
        for app in apps.get_app_configs():
            if 'django' not in app.name:
                try:
                    path = os.path.join(app.path, 'bot.py')
                    module = imp.load_source('%s.bot' % (app.name), path)
                    for name, cls in inspect.getmembers(module, inspect.isclass):
                        if (cls != SlackBot and issubclass(cls, SlackBot)):
                            try:
                                bot = Bot.objects.get(class_name=name)
                                bot.class_name = cls.__name__
                                bot.module_name = module.__name__
                                bot.description = cls.DESCRIPTION
                            except Bot.DoesNotExist:
                                bot = Bot(class_name=cls.__name__,
                                          module_name=module.__name__,
                                          description=cls.DESCRIPTION)
                            bot.save()
                except IOError as ex:
                    if ex.errno != 2:
                        raise
