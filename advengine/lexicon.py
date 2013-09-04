class Lexicon:
    def __init__(self, wordlists=[]):
        self.synonyms = {}

        for wordlist in wordlists:
            self.add_words(wordlist)


    def add_words(self, wordlist):
        """Given a list of words, create or update the entry for each,
        containing the given words and any existing synonyms for any of them."""
        # create list of new words + synonyms of all existing words
        allwords = set(wordlist)
        for word in wordlist:
            allwords |= self.synonyms.setdefault(word, set())

        # assign list to each word in list
        self.synonyms.update({word: allwords for word in allwords})


    def words_match(self, word1, word2):
        """Check if one word a synonym of the other."""
        return word1 == word2 or word1 in self[word2]


    def __getitem__(self, word):
        """Return the list of synonyms for the given word."""
        return self.synonyms.get(word, [word])
