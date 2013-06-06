class Lexicon:
    def __init__(self, wordlists=[]):
        self.synonyms = {}
        
        for wordlist in wordlists:
            self.add_words(wordlist)
            
            
    def add_words(self, wordlist):
        # create list of new words + synonyms of all existing words
        allwords = set(wordlist)
        for word in wordlist:
            allwords |= self.synonyms.setdefault(word, set())
        
        # assign list to each word in list
        self.synonyms.update({word: allwords for word in allwords})
        
        
    def words_match(self, word1, word2):
        return word1 == word2 or word1 in self[word2]
        

    def __getitem__(self, word):
        return self.synonyms.get(word, [word])