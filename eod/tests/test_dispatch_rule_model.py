from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from eod.models import Team, DispatchRule, get_teams_with_matching_rule, FIXED_TIME_EOD_MAIL_RULE


class DispatchRuleTestCase(TestCase):
    def test_should_return_teams_matching_given_rule_and_time(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        team1 = Team.objects.create(name='team1', email='team1@mailinator.com', user=user1)
        team2 = Team.objects.create(name='team2', email='team2@mailinator.com', user=user2)
        DispatchRule.objects.create(type=FIXED_TIME_EOD_MAIL_RULE, hour=9, minute=30, team=team1)
        DispatchRule.objects.create(type=FIXED_TIME_EOD_MAIL_RULE, hour=12, minute=30, team=team2)
        d3 = DispatchRule.objects.create(type=FIXED_TIME_EOD_MAIL_RULE, hour=10, minute=30, team=team2)
        current_datetime = datetime(2017, 1, 1, 10, 34, 0)

        actual_teams = get_teams_with_matching_rule(current_datetime, rule_type='FIXED_TIME_EOD_MAIL')

        self.assertEqual(len(actual_teams), 1)
        self.assertEqual(actual_teams, [team2])
