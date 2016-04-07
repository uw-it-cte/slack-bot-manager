from bot_manager.slackbot import SlackBot
from jira import JIRA
from random import randint
import re


class LinkBotSeenException(Exception): pass


class LinkBotMessage(object):
    def __init__(self, conf):
        self._conf = conf
        self._seen = []
        self._said = []

    def quip(self, link):
        try:
            quips = self._conf['QUIPS']
            while True:
                i = randint(0, len(quips) - 1)
                if i not in self._said:
                    self._said.append(i)
                    return quips[i] % link
                elif len(self._said) == len(quips):
                    self._said = []
        except:
            return link

    def message(self, link_label):
        if link_label in self._seen:
            raise LinkBotSeenException(link_label)

        self._seen.append(link_label)
        return self.build_message(self._conf['LINK'] % (link_label, link_label))

    def build_message(self, link):
        return self.quip(link)


class JiraLinkBotMessage(LinkBotMessage):
    def build_message(self, link):
        msg = self.quip(link)
        try:
            jira = JIRA(self._conf['JIRA_HOST'],
                        basic_auth=(self._conf['JIRA_LOGIN'],
                                    self._conf['JIRA_PASSWORD']))
            issue = jira.issue(ticket)
            msg += '>>> %s' % self._escape(issue.fields.summary)
        except:
            pass

        return msg

    def _escape(self, text):
        return "".join({
                            '&': '&amp;',
                            '<': '&lt;',
                            '>': '&gt;',
                            '"': '&quot;'
                }.get(c,c) for c in text)


class LinkBot(SlackBot):
    """ Implements Slack Link Bot
    """

    CONFIG = "LINKBOT_CONFIG"
    DESCRIPTION = "Turns ticket and incident tags into links"

    def process_message(self, msg):
        try:
            if msg['type'] == 'message':
                self._log.debug('message received in %s' % msg['channel'])
                for bot_conf in getattr(self.settings, self.CONFIG)['LINKBOTS']:
                    try:
                        link_class = globals()[bot_conf['LINK_CLASS']]
                    except KeyError:
                        link_class = LinkBotMessage

                    linkbot = link_class(bot_conf)

                    matches = re.findall(
                        r'(\A|\W)(%s)(\W|\Z)' % bot_conf['MATCH'],
                        msg['text'], flags=re.I)
                    for match in matches:
                        try:
                            self.post_message(msg['channel'],
                                              linkbot.message(match[1]))
                            self._log.debug(
                                'responded to link %s in %s' % (
                                    match[1], msg['channel']))
                        except LinkBotSeenException:
                            pass
        except KeyError:
            pass
