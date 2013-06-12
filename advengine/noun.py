class Noun:
    def __init__(self, ndata):
        self.data = ndata
        
        self.words = set(self.data.get('words', []))
        self.description = self.data.get('desc', '')
        self.notes = self.data.get('notes', [])
        self.is_movable = self.data.get('movable', False)
        self.is_wearable = self.data.get('wearable', False)
        
        
    def initial_locs(self):
        """Return the IDs of all nouns or rooms containing the noun at the
        start of the game."""
        return self.data.get('locs', [])