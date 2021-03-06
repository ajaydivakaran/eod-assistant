from django.core.management import BaseCommand

from eod.eod_email import send_pending_eod_mails_for_team


class Command(BaseCommand):
    help = 'Send eod mail for specified team with new eod items'

    def add_arguments(self, parser):
        parser.add_argument('team_name')

    def handle(self, *args, **options):
        send_pending_eod_mails_for_team(options['team_name'])
        self.stdout.write(self.style.SUCCESS('Done'))
