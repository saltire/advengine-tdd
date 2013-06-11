import unittest

from advengine.gamedata import GameData
from advengine.state import State
from advengine.tests import Tests


class Test_Tests(unittest.TestCase):
    def setUp(self):
        data = {'rooms': {'bedroom': {'start': True,
                                      'exits': {'south': 'kitchen'}
                                      },
                          'kitchen': {'exits': {'north': 'bedroom'}}
                          },
                'nouns': {'wallet': {'locs': ['INVENTORY'],
                                     'words': ['wallet']},
                          'blender': {'locs': ['kitchen'],
                                      'words': ['blender']}},
                'vars': {'one': 1, 'two': 2},
                'messages': {'pass': 'Pass'}
                }
        self.tests = Tests(State(GameData(data)))
        
        
    def test_var(self):
        self.assertTrue(self.tests.var('one', 1))
        

    def test_room(self):
        self.assertTrue(self.tests.room('bedroom'))
        
        
    def test_visited(self):
        self.assertTrue(self.tests.visited('bedroom'))
        
    
    def test_exitexists(self):
        self.assertTrue(self.tests.exitexists('south'))
        self.assertFalse(self.tests.exitexists('north'))
        
        
    def test_carrying(self):
        self.assertTrue(self.tests.carrying('wallet'))
        self.assertFalse(self.tests.carrying('blender'))


    def test_carrying_with_piped_filter(self):
        self.assertTrue(self.tests.carrying('blender|wallet'))
        
        
    def test_nounloc(self):
        self.assertTrue(self.tests.nounloc('blender', 'kitchen'))
        self.assertFalse(self.tests.nounloc('blender', 'bedroom'))
        self.assertTrue(self.tests.nounloc('blender|wallet', 'kitchen|bedroom'))
        
        
    def test_ininv(self):
        self.assertTrue(self.tests.ininv('wallet'))
        self.assertFalse(self.tests.ininv('blender'))
        
        
    