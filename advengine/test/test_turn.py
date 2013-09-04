import unittest

from advengine.turn import Turn


class Test_Turn(unittest.TestCase):
    def setUp(self):
        self.turn = Turn('test the command')


    def test_turn_returns_list_of_words(self):
        self.assertEqual(self.turn.words, ['test', 'command'])


    def test_words_are_updated_when_command_is_replaced(self):
        self.turn.replace_command('brand new command')
        self.assertEqual(self.turn.words, ['brand', 'new', 'command'])
