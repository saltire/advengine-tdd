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
                'vars': {'number': 2},
                'words': [['command', 'input']
                          ]
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
        
        
    def test_passing_command_to_state_makes_current_command_available(self):
        self.state.start_turn('test command')
        self.assertEqual(self.state.current_turn.command, 'test command')
        
        
    def test_command_matches_when_words_same_as_current_command(self):
        self.state.start_turn('test command')
        self.assertTrue(self.state.command_matches('test command'))
        
        
    def test_command_matches_and_ignores_articles_and_capitalization(self):
        self.state.start_turn('tEst the COMMAND')
        self.assertTrue(self.state.command_matches('Test A Command'))
        
        
    def test_command_matches_when_synonyms_used(self):
        self.state.start_turn('test command')
        self.assertTrue(self.state.command_matches('test input'))

    
    def test_command_doesnt_match_when_more_or_less_words_than_command(self):
        self.state.start_turn('test command')
        self.assertFalse(self.state.command_matches('test command extra words'))
        self.assertFalse(self.state.command_matches('test'))
        
        
    def test_command_matches_using_asterisk_wildcard(self):
        self.state.start_turn('test command')
        self.assertTrue(self.state.command_matches('test *'))
        
        
    
        
        
    