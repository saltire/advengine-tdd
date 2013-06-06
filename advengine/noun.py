class Noun:
    def __init__(self, ndata):
        self.data = ndata
        
        
    def initial_locs(self):
        """Return the IDs of all nouns or rooms containing the noun at the
        start of the game."""
        return self.data.get('locs', [])