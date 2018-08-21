import os

from django.core.management.base import BaseCommand, CommandError
from uw_gws import GWS
from slacker import Slacker
from six.moves import html_parser


class Command(BaseCommand):
    help = 'Synchronize UW Groups to Slack'

    def handle(self, *args, **options):

        slack = Slacker(os.environ.get('SLACK_API_TOKEN'))

        response = slack.usergroups.list()
        slack_groups = {}
        for usergroup in response.body['usergroups']:
            self.stdout.write(usergroup['handle'])
            slack_groups[usergroup['handle']] = usergroup

        response = slack.users.list()
        slack_users = {}
        for user in response.body['members']:
            if user['deleted'] != False:
                continue
            if 'email' not in user['profile']:
                continue
            self.stdout.write(
                "%s\t%s\t%s" % (user['name'], user['profile']['display_name'],
                                user['profile']['email']))
            slack_users[user['profile']['email']] = user

        gws = GWS()

        gws_groups = {}

        response = gws.search_groups(stem='u_classrm_services_serviceteam')
        for gws_group in response:
            if isinstance(gws_group.name, tuple):
                gws_group.name = gws_group.name[0]
            self.stdout.write(gws_group.name)
            handle = gws_group.name.replace(
                'u_classrm_services_serviceteam_', '')
            gws_groups[handle] = gws.get_group_by_id(gws_group.name)

        gws_groups['help-desk'] = gws.get_group_by_id(
            'u_classrm_services_function_classroom')

        gws_groups['cte-all'] = gws.get_group_by_id('u_classrm_employees_all')

        gws_groups['lt-all'] = gws.get_group_by_id('uw_lt')

        gws_groups['ctl-all'] = gws.get_group_by_id(
            'u_classrm_services_slack_ctl')

        h = html_parser.HTMLParser()

        for handle in gws_groups:
            gws_group = gws_groups[handle]
            if handle not in slack_groups:
                response = slack.usergroups.create(
                    name=h.unescape(gws_group.display_name),
                    handle=handle,
                    description=h.unescape(gws_group.description))
                groupid = response.body['usergroup']['id']
            else:
                groupid = slack_groups[handle]['id']
                slack.usergroups.update(
                    groupid,
                    name=h.unescape(gws_group.display_name),
                    description=h.unescape(gws_group.description))

            gws_members = gws.get_effective_members(gws_group.name)
            memberids = []
            for member in gws_members:
                if member.type != 'uwnetid':
                    continue
                self.stdout.write("\t%s" % member.name)

                email = "%s@uw.edu" % member.name
                if email in slack_users:
                    memberids.append(slack_users[email]['id'])

            response = slack.usergroups.users.update(usergroup=groupid,
                                                     users=memberids)

        # self.stdout.write(self.style.SUCCESS('netid "%s"' % uwnetid))
