import unittest

from advengine.dictionary import Dictionary


class Test_Dictionary(unittest.TestCase):
    
    def setUp(self):
        words = [['one', 'un', 'uno', 'ichi'],
                 ['red', 'rouge', 'rojo'],
                 ['good', 'great', 'awesome']
                 ]
        self.dic = Dictionary(words)
        
        
    def test_init_with_words_adds_entry_for_each_word(self):
        self.assertItemsEqual(self.dic.synonyms['red'], ['red', 'rouge', 'rojo'])
        

    def test_add_words_adds_entry_for_each_word(self):
        words = ['blue', 'bleu', 'azul']
        self.dic.add_words(words)
        for word in words:
            self.assertItemsEqual(words, self.dic.synonyms[word])
            
            
    def test_adding_overlapping_wordlist_merges_wordlists(self):
        self.dic.add_words(['green', 'vert'])
        self.dic.add_words(['vert', 'verde'])
        self.assertItemsEqual(['green', 'vert', 'verde'], self.dic.synonyms['green'])
   



if __name__ == "__main__":
    unittest.main()