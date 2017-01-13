import itertools
from datetime import datetime

from django.core.mail import send_mail

from .logging import get_logger
from .models import get_not_sent_eod_items_for_teams, get_teams_with_matching_rule, mark_eod_items_as_sent, \
    get_active_teams


def _get_team_with_name(team_list, team_name):
    for team in team_list:
        if team.name == team_name:
            return team
    return None


def _send_eod_emails(teams_due_for_eod_mail_dispatch):
    logger = get_logger()
    eod_items = get_not_sent_eod_items_for_teams(teams_due_for_eod_mail_dispatch)
    if not eod_items:
        logger.info('No eod items due for dispatch')
    for team_name, grouped_eod_items in itertools.groupby(eod_items, lambda eod_item: eod_item.team.name):
        team = _get_team_with_name(teams_due_for_eod_mail_dispatch, team_name)
        eod_item_list = list(grouped_eod_items)
        try:
            send_mail('Eod mail', '%s items to be sent' % len(eod_item_list),
                      from_email='no-reply@eodassistant.com', recipient_list=[team.email])
            mark_eod_items_as_sent(eod_item_list)
            logger.info('Sent mail to %s with %s items' % (team.email, len(eod_item_list)))
        except Exception as e:
            logger.error("Exception: [%s] occurred while sending eod mail to %s" % (str(e), team.email))


def send_rule_based_eod_mails():
    teams_due_for_eod_mail_dispatch = get_teams_with_matching_rule(datetime.now())
    _send_eod_emails(teams_due_for_eod_mail_dispatch)


def send_pending_eod_mails_for_team(team_name):
    teams_due_for_eod_mail_dispatch = list(filter(lambda team: team.name == team_name, get_active_teams()))
    _send_eod_emails(teams_due_for_eod_mail_dispatch)
