import itertools

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from eodassistant.settings import FROM_EMAIL
from .date import formatted_date_in_local_timezone
from .logging import get_logger
from .models import get_not_sent_eod_items_for_teams, get_teams_with_matching_rule, mark_eod_items_as_sent, \
    get_active_teams, FIXED_TIME_EOD_MAIL_RULE


def _get_team_with_name(team_list, team_name):
    for team in team_list:
        if team.name == team_name:
            return team
    return None


def _get_current_datetime_in_team_timezone(team):
    return formatted_date_in_local_timezone(timezone.now(), team.timezone)


def _send_eod_emails(teams_due_for_eod_mail_dispatch):
    logger = get_logger()
    eod_items = get_not_sent_eod_items_for_teams(teams_due_for_eod_mail_dispatch)
    if not eod_items:
        logger.info('No eod items due for dispatch')
        return
    for team_name, grouped_eod_items in itertools.groupby(eod_items, lambda eod_item: eod_item.team.name):
        team = _get_team_with_name(teams_due_for_eod_mail_dispatch, team_name)
        eod_item_list = list(grouped_eod_items)
        _send_email(eod_item_list, logger, team)


def _send_email(eod_item_list, logger, team):
    try:
        html_message = render_to_string('eod/eod_email.html', context={'items': eod_item_list})
        subject_line = _get_subject_line(team)
        send_mail(subject_line, message='', from_email=FROM_EMAIL,
                  recipient_list=[team.email], html_message=html_message)
        mark_eod_items_as_sent(eod_item_list)
        logger.info('Sent mail to %s with %s items' % (team.email, len(eod_item_list)))
    except Exception as e:
        logger.exception("Exception: [%s] occurred while sending eod mail to %s" % (str(e), team.email))


def _get_subject_line(team):
    local_datetime = _get_current_datetime_in_team_timezone(team)
    return '%s - %s eod update' % (local_datetime.strftime("%d %B %Y"), team.name)


def send_rule_based_eod_mails():
    teams_due_for_eod_mail_dispatch = get_teams_with_matching_rule(timezone.now(), FIXED_TIME_EOD_MAIL_RULE)
    _send_eod_emails(teams_due_for_eod_mail_dispatch)


def send_pending_eod_mails_for_team(team_name):
    teams_due_for_eod_mail_dispatch = list(filter(lambda team: team.name == team_name, get_active_teams()))
    _send_eod_emails(teams_due_for_eod_mail_dispatch)
