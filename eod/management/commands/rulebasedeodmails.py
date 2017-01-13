from django.core.management import BaseCommand

from eod.eod_emailer import send_rule_based_eod_mails


class Command(BaseCommand):
    help = 'Send rule based eod mails'

    def handle(self, *args, **options):
        send_rule_based_eod_mails()
        self.stdout.write(self.style.SUCCESS('Done'))
