import unittest

from advengine.room import Room


class Test_Room(unittest.TestCase):
    
    def setUp(self):
        self.rdata = {'id': 'bedroom',
                      'name': 'Master Bedroom',
                      'shortname': 'Bedroom',
                      'desc': 'You are in the master bedroom.',
                      'notes': ['The window is open.'],
                      'exits': {'south': 'kitchen',
                                'east': 'bathroom'
                                },
                      'start': True
                      }


    def test_room_(self):
        pass


if __name__ == "__main__":
    unittest.main()