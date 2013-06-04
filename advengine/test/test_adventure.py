import unittest

from advengine.adventure import Adventure


class Test_Adventure(unittest.TestCase):
    
    def setUp(self):
        data = {'rooms': {},
                'nouns': {},
                'vars': [],
                'words': [['red', 'rouge'],
                          ['green', 'vert']
                          ],
                'messages': {'welcome': 'Welcome to the game!',
                             'startturn': 'Turn starting.',
                             'endturn': 'Turn ending.'
                             },
                'controls': {'before_game': ['message welcome'],
                             'before_turn': ['message startturn'],
                             'during_turn': [],
                             'after_turn': ['message endturn'],
                             'after_game': []
                             }
                }
        self.adv = Adventure(data)


    def test_starting_game_returns_messages_from_before_game(self):
        self.assertItemsEqual(self.adv.start_game(), ['Welcome to the game!'])


    def test_running_turn_returns_message_from_before_turn(self):
        self.adv.start_game()
        self.assertEqual(self.adv.do_command('')[0], 'Turn starting.')
        
    
    def test_running_turn_returns_message_from_end_turn(self):
        self.adv.start_game()
        self.assertEqual(self.adv.do_command('')[-1], 'Turn ending.')
        
    
    