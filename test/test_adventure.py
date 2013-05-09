import unittest

from advengine.adventure import Adventure


class Test_Adventure(unittest.TestCase):
    
    def setUp(self):
        data = {'rooms': {},
                'nouns': {},
                'vars': [],
                'words': [],
                'messages': [],
                'controls': {'before_game': {},
                             'before_turn': {},
                             'during_turn': {},
                             'after_turn': {},
                             'after_game': {}
                             }
                }
        self.adv = Adventure(data)


    def test_(self):
        pass


if __name__ == "__main__":
    unittest.main()