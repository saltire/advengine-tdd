import unittest

from advengine.room import Room


class Test_Room(unittest.TestCase):
    
    def setUp(self):
        self.room = Room({'id': 'bedroom',
                          'name': 'Master Bedroom',
                          'shortname': 'Bedroom',
                          'desc': 'You are in the master bedroom.',
                          'notes': ['The window is open.'],
                          'exits': {'south': 'kitchen',
                                    'east': 'bathroom'
                                    },
                          'start': True
                          })
