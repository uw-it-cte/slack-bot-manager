import os

from django.core.management.base import BaseCommand, CommandError
from uw_gws import GWS
from slacker import Slacker


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
            self.stdout.write(user['name'])
            slack_users[user['name']] = user

        gws = GWS()

        try:
            gws_groups = gws.search_groups(
                stem='u_classrm_services_serviceteam')
        except Exception as ex:
            raise CommandError('Could not get service team groups: %s' % ex)

        for gws_group in gws_groups:
            self.stdout.write(gws_group.name[0])

            handle = gws_group.name[0].replace(
                'u_classrm_services_serviceteam_',
                '')
            if handle not in slack_groups:
                response = slack.usergroups.create(
                    name=gws_group.title,
                    handle=handle,
                    description=gws_group.description)
                groupid = response.body['usergroup']['id']
            else:
                groupid = slack_groups[handle]['id']

            gws_members = gws.get_effective_members(gws_group.name[0])
            memberids = []
            for member in gws_members:
                if member.member_type != 'uwnetid':
                    continue
                self.stdout.write("\t%s" % member.name)

                if member.name in slack_users:
                    memberids.append(slack_users[member.name]['id'])

            response = slack.usergroups.users.update(usergroup=groupid,
                                                     users=memberids)

        # self.stdout.write(self.style.SUCCESS('netid "%s"' % uwnetid))
