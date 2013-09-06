import unittest

from advengine.actions import BaseActions
from advengine.adventure import Adventure
from advengine.tests import BaseTests


class MockActions(BaseActions):
    def message(self, msg):
        """Test action: return a capitalized version of the given string."""
        return msg.capitalize()


class MockAdventure(Adventure):
    def __init__(self, controls):
        Adventure.__init__(self, {'rooms': {'start': {'start': True}},
                                  'controls': controls},
                           BaseTests, MockActions)


class Test_Adventure(unittest.TestCase):

    def test_starting_game_returns_messages_from_before_game(self):
        adv = MockAdventure({'before_game': 'message pass'})
        self.assertIn('Pass', adv.start_game())


    def test_command_tests_before_game_are_silently_ignored(self):
        adv = MockAdventure({'before_game': {'if': 'command *', 'then': 'message fail'}})
        self.assertNotIn('Fail', adv.start_game())


    def test_running_turn_returns_message_from_before_turn(self):
        adv = MockAdventure({'before_turn': 'message pass', 'during_turn': 'message other'})
        self.assertEqual(adv.do_command('')[0], 'Pass')


    def test_running_turn_returns_message_from_after_turn(self):
        adv = MockAdventure({'during_turn': 'message other', 'after_turn': 'message pass'})
        self.assertEqual(adv.do_command('')[-1], 'Pass')


    def test_command_test_returns_then_if_true_and_else_if_false(self):
        adv = MockAdventure({'during_turn': {'if': 'command test', 'then': ['message pass'],
                                             'else': 'message fail'}})
        self.assertEqual(['Pass'], adv.do_command('test'))
        self.assertEqual(['Fail'], adv.do_command('not the same'))


    def test_commands_stop_executing_after_done_action(self):
        adv = MockAdventure({'during_turn': ['message pass',
                                             {'if': 'command test',
                                              'then': ['message pass', 'done', 'message other']},
                                             'message other']})
        self.assertEqual(adv.do_command('test'), ['Pass', 'Pass'])


    def test_gameover_stops_execution_and_runs_after_game(self):
        adv = MockAdventure({'during_turn': ['message pass',
                                             {'if': 'command test',
                                              'then': ['message pass',
                                                       'gameover',
                                                       'message other']},
                                             'message other'],
                             'after_turn': 'message other',
                             'after_game': 'message fail'})
        self.assertEqual(adv.do_command('test'), ['Pass', 'Pass', 'Fail'])


    def test_replace_restarts_execution_from_start_of_control_stage(self):
        adv = MockAdventure({'before_turn': 'message other',
                             'during_turn': [{'if': 'command new command',
                                              'then': ['message pass', 'done']},
                                             'message fail',
                                             {'if': 'command some input',
                                              'then': 'replace new command'},
                                             'message fail'],
                             'after_turn': 'message other'})
        self.assertEqual(adv.do_command('some input'), ['Other', 'Pass', 'Other'])
