import unittest

from advengine.turn import Turn


class Test_Turn(unittest.TestCase):
    def setUp(self):
        self.turn = Turn('test the command')
        
        
    def test_turn_returns_list_of_words(self):
        self.assertEqual(self.turn.words, ['test', 'command'])
        
        
    