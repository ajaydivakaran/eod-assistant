from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from .date import time_of_day

BUFFER_PERIOD_IN_SECONDS = 300
FIXED_TIME_EOD_MAIL_RULE = 'FIXED_TIME_EOD_MAIL'


def get_active_teams():
    return Team.objects.filter(is_active=True)


def get_not_sent_eod_items_for_teams(team_list):
    return EndOfDayItem.objects.filter(is_sent=False, team__in=team_list)


def _is_time_matching(rule, current_datetime):
    timedelta = (current_datetime - time_of_day(current_datetime, rule.hour, rule.minute))
    return abs(timedelta.total_seconds()) <= BUFFER_PERIOD_IN_SECONDS


def get_teams_with_matching_rule(current_datetime, rule_type):
    rules = DispatchRule.objects.filter(team__is_active=True, type=rule_type)
    return [rule.team for rule in rules if _is_time_matching(rule, current_datetime)]


def mark_eod_items_as_sent(eod_items):
    for eod_item in eod_items:
        eod_item.is_sent = True
        eod_item.save()


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    timezone = models.CharField(max_length=30, default='Asia/Kolkata')
    is_active = models.BooleanField(default=True)
    reminder_active = models.BooleanField(default=False)
    email = models.EmailField()
    user = models.OneToOneField(User)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    teams = models.ManyToManyField(Team)
    email = models.EmailField()

    def __str__(self):
        return self.display_name


class EndOfDayItem(models.Model):
    description = models.TextField()
    story_id = models.CharField(max_length=30)
    status = models.TextField()
    contributors = models.ManyToManyField(Contributor)
    created_date = models.DateTimeField('End of day item done date', auto_now=True)
    team = models.ForeignKey(Team)
    is_sent = models.BooleanField(default=False)

    def get_contributors(self):
        return [contributor.first_name for contributor in self.contributors.all()]

    def __str__(self):
        return self.story_id


def _validate_known_type(value):
    if value not in [FIXED_TIME_EOD_MAIL_RULE]:
        raise ValidationError("%s is not a known type" % value)


class DispatchRule(models.Model):
    type = models.CharField(max_length=30, validators=[_validate_known_type])
    hour = models.IntegerField()
    minute = models.IntegerField()
    team = models.ForeignKey(Team)

    def __str__(self):
        return "Rule %s: hour: %s minute: %s" % (self.type, self.hour, self.minute)
