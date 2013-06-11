class Room:
    def __init__(self, rdata):
        self.data = rdata
        
        self.exits = self.data.get('exits', {})
        self.is_start = self.data.get('start') is True
        self.has_been_visited = False


    def visit(self):
        """Set visited flag to true."""
        self.has_been_visited = True