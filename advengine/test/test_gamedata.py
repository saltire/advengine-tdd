import os
import unittest

from advengine.gamedata import GameData, GameDataError


class MockData(GameData):
    def __init__(self, data):
        # add a starting room so we won't fail validation
        data.setdefault('rooms', {})['start'] = {'start': True}
        GameData.__init__(self, data)


class Test_GameData(unittest.TestCase):
    def test_gamedata_inits_from_file(self):
        gpath = os.path.abspath(os.path.join(__file__, '../testdata.json'))
        with open(gpath) as gfile:
            data = GameData(gfile)
        self.assertTrue(hasattr(data, 'nouns'))


    def test_gamedata_inits_from_string(self):
        gpath = os.path.abspath(os.path.join(__file__, '../testdata.json'))
        with open(gpath) as gfile:
            data = GameData(gfile.read())
        self.assertTrue(hasattr(data, 'nouns'))


    def test_gamedata_inits_from_dict(self):
        data = MockData({'nouns': {}, 'rooms': {}})
        self.assertTrue(hasattr(data, 'nouns'))


    def test_control_stages_can_be_list_or_single_control(self):
        data = MockData({'controls': {'stage 1': 'action',
                                      'stage 2': {'if': 'test', 'then': 'action'},
                                      'stage 3': ['action', {'if': 'test',
                                                             'then': 'action',
                                                             'else': 'action'},
                                                  ],
                                      }})
        self.assertEqual(len(data.controls['stage 1']), 1)
        self.assertEqual(len(data.controls['stage 2']), 1)
        self.assertEqual(len(data.controls['stage 3']), 2)


    def test_variables_are_cast_to_integer(self):
        data = MockData({'vars': {'one': '1'}})
        self.assertEqual(data.vars['one'], 1)


    def test_validation_fails_with_duplicate_entity_ids(self):
        with self.assertRaises(GameDataError) as ex:
            MockData({'nouns': {'test': {}}, 'rooms': {'test': {}}})
        self.assertEqual(ex.exception.code, 1)


    def test_validation_fails_with_reserved_entity_ids(self):
        with self.assertRaises(GameDataError) as ex:
            MockData({'nouns': {'INVENTORY': {}}})
        self.assertEqual(ex.exception.code, 2)

        with self.assertRaises(GameDataError) as ex:
            MockData({'rooms': {'WORN': {}}})
        self.assertEqual(ex.exception.code, 2)


    def test_validation_fails_with_no_starting_room(self):
        with self.assertRaises(GameDataError) as ex:
            GameData({'rooms': {}})
        self.assertEqual(ex.exception.code, 3)


    def test_validation_fails_with_multiple_starting_rooms(self):
        with self.assertRaises(GameDataError) as ex:
            GameData({'rooms': {'one': {'start': True}, 'two': {'start': True}}})
        self.assertEqual(ex.exception.code, 4)



if __name__ == "__main__":
    unittest.main()
