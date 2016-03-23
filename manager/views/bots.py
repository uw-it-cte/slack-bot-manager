from django.conf import settings
from manager.models import Bot
from manager.views import RESTDispatch
import os


def bot_is_active(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False

    return True


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
                        bot.changed_by = request.user.username
                        bot.changed_date = datetime.utcnow().replace(tzinfo=utc)
                        bot.save()
                        self._log.info('%s started Bot "%s"' % (
                            bot.changed_by, bot.name))
                                       
                    elif bot.is_active:
                        ### stop bot
                        bot.is_active = False
                        self._log.info('%s stopped Bot "%s"' % (
                            bot.changed_by, bot.name)

            return self.json_response(json.dumps({'bot': bot.json_data()}))
        except Bot.DoesNotExist:
            return self.json_response(
                '{"error":"bot %s not found"}' % bot_id, status=404)


class BotListView(RESTDispatch):
    """ Retrieves a list of Bots.
    """
    def GET(self, request, **kwargs):
        bots = []
        for bot in Bot.objects.all().order_by('name'):
            bot.is_active = is_active(bot.pid)
            bots.append(bot.json_data())

        return self.json_response(json.dumps({'bots': bots}))
