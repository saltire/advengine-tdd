import os
import unittest

from advengine.gamedata import GameData


class Test_DataFile(unittest.TestCase):
    def test_gamedata_inits_from_file(self):
        data = GameData(os.path.abspath(os.path.join(__file__,
                                                     '../testdata.json')))
        self.assertTrue(hasattr(data, 'nouns'))


    def test_gamedata_inits_from_string(self):
        data = GameData({'nouns': {}, 'rooms': {}})
        self.assertTrue(hasattr(data, 'nouns'))
        
        
    def test_control_stages_can_be_list_or_single_control(self):
        data = GameData({'controls': {'stage 1': 'action',
                                      'stage 2': {'if': 'test',
                                                  'then': 'action'},
                                      'stage 3': ['action',
                                                  {'if': 'test',
                                                   'then': 'action',
                                                   'else': 'action'}
                                                  ]
                                      }
                         })
        self.assertEqual(len(data.controls['stage 1']), 1)
        self.assertEqual(len(data.controls['stage 2']), 1)
        self.assertEqual(len(data.controls['stage 3']), 2)



if __name__ == "__main__":
    unittest.main()