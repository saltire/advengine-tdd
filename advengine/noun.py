class Noun:
    def __init__(self, ndata):
        self.data = ndata
        
        
    def initial_locs(self):
        return self.data.get('locs', [])