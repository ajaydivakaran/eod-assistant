from django.contrib.auth.models import User
from django.test import TestCase

from eod.models import Team, Contributor, \
    EndOfDayItem, get_not_sent_eod_items_for_teams, mark_eod_items_as_sent


class EndOfDayItemTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        team1 = Team.objects.create(name='team1', is_active=True, email='team1@mailinator.com', user=user1)
        team2 = Team.objects.create(name='team2', is_active=True, email='team2@mailinator.com', user=user2)
        c1 = Contributor.objects.create(first_name='John', last_name='Doe', display_name='johnDoe')
        c1.teams = [team1]
        c1.save()
        c2 = Contributor.objects.create(first_name='Jane', last_name='Doe', display_name='janeDoe')
        c2.teams = [team1]
        c2.save()
        c3 = Contributor.objects.create(first_name='Ram', last_name='Doe', display_name='ramDoe')
        c3.teams = [team2]
        c3.save()
        e1 = EndOfDayItem.objects.create(description='d1', story_id='s1', status='s1', team=team1, is_sent=True)
        e1.contributors = [c1, c2]
        e1.save()
        e2 = EndOfDayItem.objects.create(description='d2', story_id='s2', status='s2', team=team1)
        e2.contributors = [c1, c2]
        e2.save()
        e3 = EndOfDayItem.objects.create(description='d3', story_id='s3', status='s3', team=team2)
        e3.contributors = [c3]
        e3.save()

    def test_should_mark_eods_as_sent(self):
        team1 = Team.objects.get(name='team1')
        team2 = Team.objects.get(name='team2')

        actual_eod_items = list(get_not_sent_eod_items_for_teams([team1, team2]))

        self.assertEqual(len(actual_eod_items), 2)

        mark_eod_items_as_sent(actual_eod_items)

        self.assertEqual(len(get_not_sent_eod_items_for_teams([team1, team2])), 0)

    def test_should_return_not_sent_eod_items_for_given_teams(self):
        team1 = Team.objects.get(name='team1')
        team2 = Team.objects.get(name='team2')

        actual_eod_items = list(get_not_sent_eod_items_for_teams([team1, team2]))

        self.assertEqual(len(actual_eod_items), 2)
        self.assertEqual(actual_eod_items[0].story_id, 's2')
        self.assertEqual(actual_eod_items[1].story_id, 's3')
