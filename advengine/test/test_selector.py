import unittest

from advengine.actions import BaseActions
from advengine.gamedata import GameData
from advengine.selector import selector
from advengine.state import State
from advengine.tests import BaseTests


class MockTests(BaseTests):
    @selector('noun')
    def noun_starts_with_t(self, nouns):
        return any(noun for noun in nouns if noun.name.lower()[0] == 't')


    @selector('entity')
    def starts_with_t(self, entities):
        return any(entity for entity in entities if entity.name.lower()[0] == 't')


    @selector('entity', 'entity')
    def name_longer_than(self, entities1, entities2):
        return any(any(len(entity1.name) > len(entity2.name) for entity1 in entities1)
                   for entity2 in entities2)


class MockActions(BaseActions):
    @selector('noun')
    def select_nouns(self, nouns):
        return nouns


    @selector('entity')
    def select_entities(self, entities):
        return entities


    @selector('noun', 'room')
    def select_nouns_and_rooms(self, nouns, rooms):
        return (nouns, rooms)


class Test_Selector(unittest.TestCase):
    def setUp(self):
        data = {'nouns': {'table': {'name': 'Table', 'words': ['desk']},
                          'chair': {'name': 'Chair', 'locs': ['throneroom']},
                          },
                'rooms': {'throneroom': {'name': 'Throne room', 'start': True},
                          'dungeon': {'name': 'Dungeon'},
                          },
                }
        gamedata = GameData(data)
        state = State(gamedata)
        self.tests = MockTests(state)
        self.actions = MockActions(state, self.tests)

        self.table = state.nouns['table']
        self.chair = state.nouns['chair']
        self.throneroom = state.rooms['throneroom']
        self.dungeon = state.rooms['dungeon']


    def test_blank_selector_returns_all(self):
        self.assertItemsEqual(self.actions.select_entities(''),
                              [self.table, self.chair, self.throneroom, self.dungeon])


    def test_selector_passes_objects_to_function(self):
        self.assertItemsEqual(self.actions.select_nouns('table'), [self.table])


    def test_selector_splits_piped_string(self):
        self.assertItemsEqual(self.actions.select_entities('table|throneroom'),
                              [self.table, self.throneroom])


    def test_selector_replaces_numerical_wildcard(self):
        self.tests.state.start_turn('examine desk')
        self.assertItemsEqual(self.actions.select_nouns('%2'), [self.table])


    def test_selector_takes_multiple_types(self):
        nouns, rooms = self.actions.select_nouns_and_rooms('chair', 'dungeon|throneroom')
        self.assertItemsEqual(nouns, [self.chair])
        self.assertItemsEqual(rooms, [self.dungeon, self.throneroom])


    def test_selector_filters_by_type(self):
        self.assertItemsEqual(self.actions.select_nouns('table|throneroom'), [self.table])


    def test_selector_filters_by_passed_test(self):
        self.assertItemsEqual(self.actions.select_nouns('chair|table:starts_with_t'), [self.table])


    def test_selector_filters_by_passed_tests_type(self):
        self.assertItemsEqual(self.actions.select_entities('throneroom|table:noun_starts_with_t'),
                              [self.table])


    def test_asterisk_or_blank_selects_all_items_of_selector_type(self):
        self.assertItemsEqual(self.actions.select_nouns('*'), self.actions.select_nouns(''),
                              [self.table, self.chair])


    def test_asterisk_or_blank_before_filter_selects_all_items_that_pass_filter(self):
        self.assertItemsEqual(self.actions.select_entities(':starts_with_t'),
                              self.actions.select_entities('*:starts_with_t'),
                              [self.table, self.throneroom])


    def test_two_argument_filter_takes_second_selector_in_parens(self):
        self.assertItemsEqual(self.actions.select_entities(':name_longer_than(dungeon)'),
                              [self.throneroom])


    def test_two_argument_filter_is_ignored_if_no_parens(self):
        self.assertItemsEqual(self.actions.select_entities(':name_longer_than'),
                              [self.table, self.chair, self.throneroom, self.dungeon])


    def test_two_argument_filter_uses_all_for_blank_second_selector(self):
        self.assertItemsEqual(self.actions.select_entities(':name_longer_than()'),
                              [self.throneroom, self.dungeon])

