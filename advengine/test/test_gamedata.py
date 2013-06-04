import os
import unittest

from advengine.gamedata import GameData


class Test_DataFile(unittest.TestCase):
    def test_gamedata_inits_from_file(self):
        data = GameData(os.path.abspath(os.path.join(__file__,
                                                     '../test_data.json')))
        self.assertTrue(hasattr(data, 'nouns'))


    def test_gamedata_inits_from_string(self):
        data = GameData({'nouns': {}, 'rooms': {}})
        self.assertTrue(hasattr(data, 'nouns'))



if __name__ == "__main__":
    unittest.main()