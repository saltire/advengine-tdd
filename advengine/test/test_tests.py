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
                                     'words': ['wallet'],
                                     'movable': True},
                          'money': {'locs': ['wallet'],
                                    'desc': "You're rich!",
                                    'notes': ['pass'],
                                    'movable': True},
                          'hat': {'locs': ['WORN'],
                                  'words': ['wallet'],
                                  'movable': True,
                                  'wearable': True},
                          'blender': {'locs': ['kitchen'],
                                      'words': ['blender']},
                          'window': {'locs': ['bedroom', 'kitchen']},
                          'nothing': {}
                          },      
                'vars': {'one': 1, 'two': 2},
                'messages': {'pass': 'Pass'}
                }
        self.tests = Tests(State(GameData(data)))
        
        
    def test_variable_equals(self):
        self.assertTrue(self.tests.var('one', 1))
        self.assertTrue(self.tests.var('one', '1'))
        self.assertTrue(self.tests.var('one', '=1'))
        self.assertFalse(self.tests.var('one', 2))
        self.assertFalse(self.tests.var('one', '2'))
        
        
    def test_variable_less_than_or_greater_than(self):
        self.assertTrue(self.tests.var('one', '<2'))
        self.assertFalse(self.tests.var('one', '<0'))
        self.assertTrue(self.tests.var('one', '>0'))
        self.assertFalse(self.tests.var('one', '>2'))
        

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
        self.assertTrue(self.tests.nounloc('money', 'wallet'))
        
        
    def test_ininv(self):
        self.assertTrue(self.tests.ininv('wallet'))
        self.assertFalse(self.tests.ininv('blender'))
        
        
    def test_worn(self):
        self.assertTrue(self.tests.worn('hat'))
        self.assertFalse(self.tests.worn('blender'))
        
        
    def test_inroom(self):
        self.assertTrue(self.tests.inroom('window'))
        self.assertFalse(self.tests.inroom('hat'))
        
        
    def test_present(self):
        self.assertTrue(self.tests.present('window'))
        self.assertTrue(self.tests.present('hat'))
        self.assertTrue(self.tests.present('wallet'))
        self.assertTrue(self.tests.present('money'))
        self.assertFalse(self.tests.present('blender'))
        
        
    def test_contained(self):
        self.assertTrue(self.tests.contained('money'))
        self.assertFalse(self.tests.contained('window'))
        self.assertFalse(self.tests.contained('hat'))
        self.assertFalse(self.tests.contained('wallet'))
        
        
    def test_somewhere(self):
        self.assertTrue(self.tests.somewhere('money'))
        self.assertTrue(self.tests.somewhere('window'))
        self.assertTrue(self.tests.somewhere('hat'))
        self.assertTrue(self.tests.somewhere('wallet'))
        self.assertFalse(self.tests.somewhere('nothing'))
        
        
    def test_movable(self):
        self.assertTrue(self.tests.movable('wallet'))
        self.assertFalse(self.tests.movable('window'))
        
        
    def test_wearable(self):
        self.assertTrue(self.tests.wearable('hat'))
        self.assertFalse(self.tests.wearable('blender'))
        
        
    def test_hasdesc(self):
        self.assertTrue(self.tests.hasdesc('money'))
        self.assertFalse(self.tests.hasdesc('wallet'))
        
        
    def test_hasnotes(self):
        self.assertTrue(self.tests.hasnotes('money'))
        self.assertFalse(self.tests.hasnotes('wallet'))
        
        
    def test_hascontents(self):
        self.assertTrue(self.tests.hascontents('wallet'))
        self.assertFalse(self.tests.hascontents('money'))
        

    def test_random(self):
        self.assertIn(self.tests.random(50), (True, False))

