from django.contrib.auth.models import User
from django.test import TestCase

from eod.models import Team, get_active_teams


class TeamTestCase(TestCase):
    def test_should_return_active_teams(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        Team.objects.create(name='team1', is_active=False, email='team1@mailinator.com', user=user1)
        team2 = Team.objects.create(name='team2', is_active=True, email='team2@mailinator.com', user=user2)

        active_teams = list(get_active_teams())

        self.assertEqual(len(active_teams), 1)
        self.assertEqual(active_teams, [team2])
