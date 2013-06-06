import unittest

from advengine.gamedata import GameData
from advengine.state import State
from advengine.tests import Tests


class Test_Tests(unittest.TestCase):
    def setUp(self):
        data = GameData({'vars': {'one': 1, 'two': 2},
                         'messages': {'pass': 'Pass'}
                         })
        self.tests = Tests(State(data))
        
        
    def test_variable(self):
        self.assertTrue(self.tests.var('one', 1))
        
