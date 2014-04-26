import unittest

from advengine.gamedata import GameData
from advengine.state import State
from advengine.tests import Tests


class Test_Tests(unittest.TestCase):
    def setUp(self):
        data = {'rooms': {'bedroom': {'start': True,
                                      'exits': {'south': 'kitchen'},
                                      },
                          'kitchen': {'exits': {'north': 'bedroom'}},
                          },
                'nouns': {'wallet': {'locs': ['INVENTORY'],
                                     'words': ['wallet'],
                                     'movable': True,
                                     },
                          'money': {'locs': ['wallet'],
                                    'desc': "You're rich!",
                                    'notes': ['pass'],
                                    'movable': True,
                                    },
                          'hat': {'locs': ['WORN'],
                                  'words': ['wallet'],
                                  'movable': True,
                                  'wearable': True,
                                  },
                          'blender': {'locs': ['kitchen'],
                                      'words': ['blender'],
                                      },
                          'window': {'locs': ['bedroom', 'kitchen']},
                          'nothing': {},
                          },
                'vars': {'one': 1, 'two': 2},
                'messages': {'pass': 'Pass'},
                'words': [['north', 'n'], ['south', 's']]
                }
        self.state = State(GameData(data))
        self.tests = Tests(self.state)


    def test_any_returns_true_for_any_selector_with_at_least_one_result(self):
        self.assertTrue(self.tests.any(''))
        self.assertTrue(self.tests.any('hat'))
        self.assertTrue(self.tests.any('hat|bedroom'))
        self.assertTrue(self.tests.any('fake|bedroom'))
        self.assertTrue(self.tests.any('fake|hat'))
        self.assertFalse(self.tests.any('pass'))


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
        self.assertTrue(self.tests.var('one', '>=0'))
        self.assertTrue(self.tests.var('one', '>=1'))
        self.assertFalse(self.tests.var('one', '>=2'))
        self.assertFalse(self.tests.var('one', '<=0'))
        self.assertTrue(self.tests.var('one', '<=1'))
        self.assertTrue(self.tests.var('one', '<=2'))


    def test_room(self):
        self.assertTrue(self.tests.room('bedroom'))


    def test_visited(self):
        self.assertTrue(self.tests.visited('bedroom'))


    def test_exitexists(self):
        self.assertTrue(self.tests.exitexists('south'))
        self.assertFalse(self.tests.exitexists('north'))


    def test_exitexists_with_synonym(self):
        self.assertTrue(self.tests.exitexists('s'))
        self.assertFalse(self.tests.exitexists('n'))


    def test_exitexists_with_numerical_wildcard(self):
        self.state.start_turn('go south')
        self.assertTrue(self.tests.exitexists('%2'))
        self.state.start_turn('go east')
        self.assertFalse(self.tests.exitexists('%2'))


    def test_carrying_with_no_arguments_returns_true_if_carrying_anything(self):
        self.assertTrue(self.tests.carrying())
        self.state.remove_noun(self.state.nouns['wallet'], 'INVENTORY')
        self.assertFalse(self.tests.carrying())


    def test_wearing_with_no_arguments_returns_true_if_wearing_anything(self):
        self.assertTrue(self.tests.wearing())
        self.state.remove_noun(self.state.nouns['hat'], 'WORN')
        self.assertFalse(self.tests.wearing())


    def test_carrying(self):
        self.assertTrue(self.tests.carrying('wallet'))
        self.assertFalse(self.tests.carrying('blender'))


    def test_carrying_with_piped_filter(self):
        self.assertTrue(self.tests.carrying('blender|wallet'))


    def test_carrying_with_numerical_wildcard(self):
        self.state.start_turn('examine wallet')
        self.assertTrue(self.tests.carrying('%2'))
        self.state.start_turn('examine blender')
        self.assertFalse(self.tests.carrying('%2'))


    def test_nounloc(self):
        self.assertTrue(self.tests.nounloc('blender', 'kitchen'))
        self.assertFalse(self.tests.nounloc('blender', 'bedroom'))
        self.assertTrue(self.tests.nounloc('blender|wallet', 'kitchen|bedroom'))
        self.assertTrue(self.tests.nounloc('money', 'wallet'))


    def test_wearing(self):
        self.assertTrue(self.tests.wearing('hat'))
        self.assertFalse(self.tests.wearing('blender'))


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
