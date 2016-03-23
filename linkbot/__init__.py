from django.conf import settings
from manager import SlackBotManager
from slacker import Slacker
from websocket import create_connection
from random import randint
import simplejson as json
import re


class LinkBot(SlackBotManager):
    """ Implements Slack Link Bot
    """

    self.name = 'Link Bot'
    self.description = 'Matches tokens in messages and responding with links'

    def bot(self):
        slack = Slacker(self._api_token)
        response = slack.rtm.start()
        websocket = create_connection(response.body['url'])
        while True:
            try:
                rcv = websocket.recv()
                j = json.loads(rcv)
                if j['type'] == 'message':
                    for tag, link, quips in getattr(settings, 'LINK_MATCHES', []):
                        match = tag.match(j['text'])
                        if match:
                            quip = quips[randint(0,len(quips)-1)] if quips else '%s'
                            slack.chat.post_message(
                                j['channel'],
                                (quip) % (link % (match.group(2), match.group(2))),
                                as_user=j['user'],
                                parse='none')
                            break
            except KeyError:
                pass
