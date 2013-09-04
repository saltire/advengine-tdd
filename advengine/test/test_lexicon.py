import unittest

from advengine.lexicon import Lexicon


class Test_Thesaurus(unittest.TestCase):

    def setUp(self):
        words = [['one', 'un', 'uno', 'ichi'],
                 ['red', 'rouge', 'rojo'],
                 ['good', 'great', 'awesome']
                 ]
        self.lex = Lexicon(words)


    def test_init_with_words_adds_entry_for_each_word(self):
        self.assertItemsEqual(self.lex['red'],
                              ['red', 'rouge', 'rojo'])


    def test_add_words_adds_entry_for_each_word(self):
        words = ['blue', 'bleu', 'azul']
        self.lex.add_words(words)
        for word in words:
            self.assertItemsEqual(self.lex[word], words)


    def test_adding_overlapping_wordlist_merges_wordlists(self):
        self.lex.add_words(['green', 'vert'])
        self.lex.add_words(['vert', 'verde'])
        self.assertItemsEqual(self.lex['verde'],
                              ['green', 'vert', 'verde'])


    def test_word_match_returns_true_for_synonyms(self):
        self.lex.add_words(['green', 'vert'])
        self.assertTrue(self.lex.words_match('green', 'vert'))
        self.assertTrue(self.lex.words_match('vert', 'green'))
