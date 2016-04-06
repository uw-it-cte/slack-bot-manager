from django.conf import settings
from logging import getLogger
from slacker import Slacker
from websocket import create_connection
import json


class SlackBot(object):

    SETTINGS = None
    DESCRIPTION = "base class"

    def __init__(self, logger=None):
        api_token = getattr(settings, self.SETTINGS)['API_TOKEN']
        self._slack = Slacker(api_token)
        self._robo_id = self._slack.auth.test().body.get('user_id')
        self._websocket = None
        self._log = logger if logger else getLogger(__name__)

    def bot(self):
        while True:
            msg = self.get_real_time_message()
            if not msg:
                return

            self.process_message(msg)

    def process_message(self, msg):
        try:
            self.post_message(msg['channel'], 'I got a message!')
        except:
            pass

    def get_real_time_message(self):
        if not self._websocket:
            response = self._slack.rtm.start()
            self._websocket = create_connection(response.body['url'])

        while True:
            try:
                msg = json.loads(self._websocket.recv())
            except Exception as ex:
                self._log.error('RTM Receive: %s' % ex)
                self._websocket.close()
                return None

            if msg.get('user', '') == self._robo_id:
                continue;

            return msg

    def post_message(self, channel, message):
        self._slack.chat.post_message(
            channel, message, as_user=self._robo_id, parse='none')
