import unittest

from advengine.gamedata import GameData
from advengine.state import State


class Test_State(unittest.TestCase):
    def setUp(self):
        data = {'rooms': {'bedroom': {'name': 'Bedroom',
                                      },
                          'kitchen': {'name': 'Kitchen',
                                      }
                          },
                'nouns': {'window': {'name': 'Window',
                                     'locs': ['bedroom', 'kitchen']
                                     },
                          'blender': {'name': 'Blender',
                                      'locs': ['kitchen']
                                      }
                          },
                'vars': {'number': 2}
                }
        
        self.state = State(GameData(data))
        
        self.bedroom = self.state.rooms['bedroom']
        self.kitchen = self.state.rooms['kitchen']

        self.window = self.state.nouns['window']
        self.blender = self.state.nouns['blender']
    
    
    def test_state_returns_all_nouns_at_location(self):
        self.assertItemsEqual(self.state.nouns_at_loc(self.kitchen),
                              [self.window, self.blender])
        self.assertItemsEqual(self.state.nouns_at_loc(self.bedroom),
                              [self.window])
    
    
    def test_state_returns_all_locations_of_noun(self):
        self.assertItemsEqual(self.state.noun_locs(self.window),
                              [self.bedroom, self.kitchen])
        
        
    def test_state_returns_variable(self):
        self.assertEqual(self.state.vars['number'], 2)