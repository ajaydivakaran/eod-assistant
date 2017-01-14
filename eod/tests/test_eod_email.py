from datetime import datetime
from unittest.mock import patch, MagicMock

from django.core import mail
from django.test import TestCase

from eod.eod_email import send_pending_eod_mails_for_team, send_rule_based_eod_mails


class EodEmailerTestCase(TestCase):
    @patch('eod.eod_email.get_active_teams')
    @patch('eod.eod_email.get_logger', )
    @patch('eod.eod_email.get_not_sent_eod_items_for_teams')
    def test_should_not_send_end_of_day_email_when_no_new_eod_items_present(self,
                                                                            get_not_sent_eod_items_for_teams_mock,
                                                                            logger_mock,
                                                                            get_active_teams_mock):
        logger_instance_mock = MagicMock()
        logger_mock.return_value = logger_instance_mock
        team1 = MagicMock()
        team1.name = 'team1'
        team1.email = 'team1@mailinator.com'
        team2 = MagicMock()
        team2.name = 'team2'
        team2.email = 'team2@mailinator.com'
        get_active_teams_mock.return_value = [team1, team2]
        get_not_sent_eod_items_for_teams_mock.return_value = []

        send_pending_eod_mails_for_team(team_name='team_1')

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(get_active_teams_mock.call_args, ())
        get_active_teams_mock.assert_called_with()
        logger_instance_mock.info.assert_called_with('No eod items due for dispatch')

    @patch('eod.eod_email.datetime')
    @patch('eod.eod_email.mark_eod_items_as_sent')
    @patch('eod.eod_email.get_active_teams')
    @patch('eod.eod_email.get_logger', )
    @patch('eod.eod_email.get_not_sent_eod_items_for_teams')
    def test_should_send_end_of_day_email_to_team_when_new_eod_items_present(self,
                                                                             get_not_sent_eod_items_for_teams_mock,
                                                                             logger_mock,
                                                                             get_active_teams_mock,
                                                                             mark_eod_items_as_sent_mock,
                                                                             datetime_mock):
        logger_instance_mock = MagicMock()
        logger_mock.return_value = logger_instance_mock
        team1 = MagicMock()
        team1.name = 'team1'
        team1.email = 'team1@mailinator.com'
        team1.timezone = 'Asia/Kolkata'
        team2 = MagicMock()
        team2.name = 'team2'
        team2.email = 'team2@mailinator.com'
        team2.timezone = 'Asia/Kolkata'
        c1 = MagicMock(first_name='John', last_name='Doe')
        c2 = MagicMock(first_name='Jane', last_name='Doe')
        get_active_teams_mock.return_value = [team1, team2]
        e1 = MagicMock(description='desc1', story_id='story_id1', status='status1', team=team1, contributors=[c1, c2])
        e2 = MagicMock(description='desc2', story_id='story_id2', status='status2', team=team1, contributors=[c2])
        datetime_mock.now.return_value = datetime(2017, 1, 1, 10, 20, 30)
        eod_item_list = [e1, e2]
        get_not_sent_eod_items_for_teams_mock.return_value = eod_item_list

        send_pending_eod_mails_for_team(team_name='team1')

        mark_eod_items_as_sent_mock.assert_called_with(eod_item_list)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '01 January 2017 - team1 eod update')
        self.assertEqual(mail.outbox[0].body, '')
        self.assertEqual(mail.outbox[0].from_email, 'no-reply@eodassistant.com')
        self.assertEqual(mail.outbox[0].recipients(), ['team1@mailinator.com'])
        logger_instance_mock.info.assert_called_with('Sent mail to team1@mailinator.com with 2 items')

    @patch('eod.eod_email.datetime')
    @patch('eod.eod_email.get_teams_with_matching_rule')
    @patch('eod.eod_email.get_logger', )
    @patch('eod.eod_email.get_not_sent_eod_items_for_teams')
    def test_should_send_end_of_day_email_to_team_with_matching_rule_when_new_eod_items_present(self,
                                                                                                get_new_eod_items_mock,
                                                                                                logger_mock,
                                                                                                get_teams_with_matching_rule,
                                                                                                datetime_mock):
        logger_instance_mock = MagicMock()
        logger_mock.return_value = logger_instance_mock
        team1 = MagicMock()
        team1.name = 'team1'
        team1.email = 'team1@mailinator.com'
        team1.timezone = 'Asia/Kolkata'
        team2 = MagicMock()
        team2.name = 'team2'
        team2.email = 'team2@mailinator.com'
        team2.timezone = 'Asia/Kolkata'
        c1 = MagicMock(first_name='John', last_name='Doe')
        c2 = MagicMock(first_name='Jane', last_name='Doe')
        get_teams_with_matching_rule.return_value = [team1]
        e1 = MagicMock(description='desc1', story_id='story_id1', status='status1', team=team1,
                       contributors=[c1, c2])
        e2 = MagicMock(description='desc2', story_id='story_id2', status='status2', team=team1, contributors=[c2])
        datetime_mock.now.return_value = datetime(2017, 1, 1, 10, 20, 30)
        get_new_eod_items_mock.return_value = [e1, e2]

        send_rule_based_eod_mails()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '01 January 2017 - team1 eod update')
        self.assertEqual(mail.outbox[0].body, '')
        self.assertEqual(mail.outbox[0].from_email, 'no-reply@eodassistant.com')
        self.assertEqual(mail.outbox[0].recipients(), ['team1@mailinator.com'])
        logger_instance_mock.info.assert_called_with('Sent mail to team1@mailinator.com with 2 items')
        get_teams_with_matching_rule.assert_called_with(datetime(2017, 1, 1, 10, 20, 30), 'FIXED_TIME_EOD_MAIL')
