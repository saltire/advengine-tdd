import unittest

from advengine.gamedata import GameData
from advengine.selector import selector
from advengine.state import State


class MockTests:
    def __init__(self):
        data = {'nouns': {'thing': {'words': ['item', 'object'], 'locs': ['place']},
                          'otherthing': {'locs': ['place']},
                          'anotherthing': {'locs': ['anotherplace']},
                          },
                'rooms': {'place': {'start': True},
                          'otherplace': {},
                          'anotherplace': {},
                          },
                }
        self.state = State(GameData(data))


    @selector('noun')
    def select_nouns(self, nouns='default'):
        return nouns


    @selector('location')
    def select_locations(self, locs):
        return locs


    @selector('entity')
    def select_entities(self, entities):
        return entities


    @selector('noun', 'room')
    def select_nouns_and_rooms(self, nouns, rooms):
        return nouns, rooms



class Test_Selector(unittest.TestCase):
    def setUp(self):
        self.tests = MockTests()

        self.thing = self.tests.state.nouns['thing']
        self.anotherthing = self.tests.state.nouns['anotherthing']

        self.place = self.tests.state.rooms['place']


    def test_noun_selector_replaced_with_list_of_nouns(self):
        self.assertItemsEqual(self.tests.select_nouns('thing'), [self.thing])


    def test_location_selector_replaced_with_list_of_locations(self):
        self.assertItemsEqual(self.tests.select_locations('thing|place|INVENTORY'),
                              [self.thing, self.place, 'INVENTORY'])


    def test_method_with_two_selectors_replaces_both(self):
        nouns, rooms = self.tests.select_nouns_and_rooms('thing', 'place')
        self.assertItemsEqual(nouns, [self.thing])
        self.assertItemsEqual(rooms, [self.place])


    def test_numeric_wildcard_replaced_with_matching_noun(self):
        self.tests.state.start_turn('examine item')
        self.assertItemsEqual(self.tests.select_entities('%2'), [self.thing])


    def test_passing_too_few_selectors_does_not_fail(self):
        self.assertEqual(self.tests.select_nouns(), 'default')


    def test_selectors_can_use_pipes(self):
        self.assertItemsEqual(self.tests.select_nouns('thing|anotherthing'),
                              [self.thing, self.anotherthing])


    def test_selectors_can_use_test_filters(self):
        self.assertItemsEqual(self.tests.select_nouns('thing|anotherthing:present'), [self.thing])




