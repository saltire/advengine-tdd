import unittest

from advengine.actions import Actions
from advengine.gamedata import GameData
from advengine.state import State


class Test_Actions(unittest.TestCase):
    def setUp(self):
        data = GameData({'vars': {'one': 1, 'two': 2},
                         'messages': {'pass': 'Pass',
                                      'subword': "Second word is %2"
                                      }
                         })
        self.state = State(data)
        self.actions = Actions(self.state)


    def test_message(self):
        self.assertEqual(self.actions.message('pass'), ['Pass'])
        

    def test_message_replaces_numerical_wildcard(self):
        self.state.start_turn('testing numbered words')
        self.assertEqual(self.actions.message('subword'),
                         ['Second word is numbered'])