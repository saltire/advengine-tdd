import os
import unittest

from advengine.datafile import DataFile


class Test_DataFile(unittest.TestCase):
    
    def setUp(self):
        path = os.path.abspath(os.path.join(__file__,
                                            '../../games/starflight.json'))
        self.datafile = DataFile(path)


    def test_data_contains_attrs(self):
        attrs = ('rooms', 'nouns', 'words', 'vars', 'controls', 'messages')
        self.assertItemsEqual(attrs, self.datafile.data.keys())



if __name__ == "__main__":
    unittest.main()