import os
import unittest

from advengine.gamedata import GameData, ParseError


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
        data = GameData({'nouns': {}, 'rooms': {}})
        self.assertTrue(hasattr(data, 'nouns'))


    def test_control_stages_can_be_list_or_single_control(self):
        data = GameData({'controls': {'stage 1': 'action',
                                      'stage 2': {'if': 'test', 'then': 'action'},
                                      'stage 3': ['action',
                                                  {'if': 'test','then': 'action','else': 'action'}
                                                  ],
                                      }
                         })
        self.assertEqual(len(data.controls['stage 1']), 1)
        self.assertEqual(len(data.controls['stage 2']), 1)
        self.assertEqual(len(data.controls['stage 3']), 2)


    def test_variables_are_cast_to_integer(self):
        data = GameData({'vars': {'one': '1'}})
        self.assertEqual(data.vars['one'], 1)


    def test_validation_fails_with_duplicate_entity_ids(self):
        self.assertRaises(ParseError, GameData, {'nouns': {'test': {}}, 'rooms': {'test': {}}})


    def test_validation_fails_with_reserved_entity_ids(self):
        self.assertRaises(ParseError, GameData, {'nouns': {'INVENTORY': {}}})
        self.assertRaises(ParseError, GameData, {'rooms': {'WORN': {}}})



if __name__ == "__main__":
    unittest.main()
