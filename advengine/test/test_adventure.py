import unittest

from advengine.adventure import Adventure


class Test_Adventure(unittest.TestCase):
    
    def setUp(self):
        self.messages = {'pass': 'Pass',
                         'fail': 'Fail',
                         'other': 'Other'}


    def test_starting_game_returns_messages_from_before_game(self):
        adv = Adventure({'controls': {'before_game': 'message pass'},
                         'messages': self.messages})
        self.assertIn('Pass', adv.start_game())
        
        
    def test_command_tests_before_game_are_silently_ignored(self):
        adv = Adventure({'controls': {'before_game': {'if': 'command *',
                                                      'then': 'message fail'}},
                         'messages': self.messages})
        self.assertNotIn('Fail', adv.start_game())

    
    def test_running_turn_returns_message_from_before_turn(self):
        adv = Adventure({'controls': {'before_turn': 'message pass',
                                      'during_turn': 'message other'},
                         'messages': self.messages})
        self.assertEqual(adv.do_command('')[0], 'Pass')
        
    
    def test_running_turn_returns_message_from_end_turn(self):
        adv = Adventure({'controls': {'during_turn': 'message other',
                                      'after_turn': 'message pass'},
                         'messages': self.messages})
        self.assertEqual(adv.do_command('')[-1], 'Pass')
        
    
    def test_command_test_returns_then_if_true_and_else_if_false(self):
        adv = Adventure({'controls': {'during_turn': {'if': 'command test',
                                                      'then': ['message pass'],
                                                      'else': 'message fail'}},
                         'messages': self.messages})
        self.assertEqual(['Pass'], adv.do_command('test'))
        self.assertEqual(['Fail'], adv.do_command('not the same'))
        
        
    def test_commands_stop_executing_after_done_action(self):
        adv = Adventure({'controls': {'during_turn': ['message pass',
                                                      {'if': 'command test',
                                                       'then': ['message pass',
                                                                'done',
                                                                'message other']
                                                       },
                                                      'message other']},
                         'messages': self.messages})
        self.assertItemsEqual(adv.do_command('test'), ['Pass', 'Pass'])
        
    