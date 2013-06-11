import unittest

from advengine.adventure import Adventure


def init_adventure(controls):
    return Adventure({'rooms': {'start': {'start': True}},
                      'controls': controls,
                      'messages': {'pass': 'Pass',
                                   'fail': 'Fail',
                                   'other': 'Other'}
                      })


class Test_Adventure(unittest.TestCase):

    def test_starting_game_returns_messages_from_before_game(self):
        adv = init_adventure({'before_game': 'message pass'})
        self.assertIn('Pass', adv.start_game())
        
        
    def test_command_tests_before_game_are_silently_ignored(self):
        adv = init_adventure({'before_game': {'if': 'command *',
                                              'then': 'message fail'}})
        self.assertNotIn('Fail', adv.start_game())

    
    def test_running_turn_returns_message_from_before_turn(self):
        adv = init_adventure({'before_turn': 'message pass',
                              'during_turn': 'message other'})
        self.assertEqual(adv.do_command('')[0], 'Pass')
        
    
    def test_running_turn_returns_message_from_end_turn(self):
        adv = init_adventure({'during_turn': 'message other',
                              'after_turn': 'message pass'})
        self.assertEqual(adv.do_command('')[-1], 'Pass')
        
    
    def test_command_test_returns_then_if_true_and_else_if_false(self):
        adv = init_adventure({'during_turn': {'if': 'command test',
                                              'then': ['message pass'],
                                              'else': 'message fail'}})
        self.assertEqual(['Pass'], adv.do_command('test'))
        self.assertEqual(['Fail'], adv.do_command('not the same'))
        
        
    def test_commands_stop_executing_after_done_action(self):
        adv = init_adventure({'during_turn': ['message pass',
                                              {'if': 'command test',
                                               'then': ['message pass',
                                                        'done',
                                                        'message other']
                                               },
                                              'message other']})
        self.assertItemsEqual(adv.do_command('test'), ['Pass', 'Pass'])
        
    