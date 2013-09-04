import unittest

from advengine.gamedata import GameData
from advengine.state import State


class Test_State(unittest.TestCase):
    def setUp(self):
        data = {'rooms': {'bedroom': {'start': True},
                          'kitchen': {}
                          },
                'nouns': {'window': {'locs': ['bedroom', 'kitchen']},
                          'blender': {'locs': ['kitchen'],
                                      'words': ['blender', 'processor', 'item']
                                      },
                          'wallet': {'locs': ['INVENTORY'],
                                     'words': ['wallet', 'item']}
                          },
                'vars': {'number': 2},
                'words': [['command', 'input']]
                }

        self.state = State(GameData(data))

        for rid, room in self.state.rooms.items():
            setattr(self, rid, room)
        for nid, noun in self.state.nouns.items():
            setattr(self, nid, noun)


    def test_state_returns_all_nouns_at_location(self):
        self.assertItemsEqual(self.state.nouns_at_loc(self.kitchen),
                              [self.window, self.blender])
        self.assertItemsEqual(self.state.nouns_at_loc(self.bedroom),
                              [self.window])
        self.assertItemsEqual(self.state.nouns_at_loc(self.bedroom, 'INVENTORY'),
                              [self.window, self.wallet])


    def test_state_returns_all_locations_of_noun(self):
        self.assertItemsEqual(self.state.noun_locs(self.window),
                              [self.bedroom, self.kitchen])
        self.assertItemsEqual(self.state.noun_locs(self.window, self.wallet),
                              [self.bedroom, self.kitchen, 'INVENTORY'])


    def test_state_returns_nouns_by_words_only(self):
        self.assertItemsEqual(self.state.nouns_by_word('item'),
                              [self.blender, self.wallet])
        self.assertItemsEqual(self.state.nouns_by_word('window'), [])


    def test_state_returns_nouns_by_numeric_wildcard(self):
        self.state.start_turn('examine item')
        self.assertItemsEqual(self.state.nouns_by_input_word(2),
                              [self.blender, self.wallet])


    def test_state_returns_initial_room(self):
        self.assertEqual(self.state.current_room, self.bedroom)


    def test_initial_room_visited_at_start_of_game(self):
        self.assertTrue(self.state.current_room.has_been_visited)


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


    def test_state_adds_noun_to_location(self):
        self.state.add_noun(self.blender, self.bedroom)
        self.assertItemsEqual(self.state.noun_locs(self.blender),
                              [self.bedroom, self.kitchen])


    def test_state_removes_noun_from_location(self):
        self.state.remove_noun(self.window, self.bedroom)
        self.assertItemsEqual(self.state.noun_locs(self.window), [self.kitchen])


    def test_state_moves_noun_from_one_location_to_another(self):
        self.state.move_noun(self.blender, self.bedroom)
        self.assertItemsEqual(self.state.noun_locs(self.blender),
                              [self.bedroom])


    def test_state_removes_noun_from_all_locations(self):
        self.state.clear_noun_locs(self.window)
        self.assertItemsEqual(self.state.noun_locs(self.window), [])
