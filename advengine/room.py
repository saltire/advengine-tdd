class Room:
    def __init__(self, rdata):
        self.data = rdata
        
        self.description = self.data.get('desc', None)
        self.notes = self.data.get('notes', [])
        self.exits = self.data.get('exits', {})
        self.is_start = self.data.get('start') is True
        self.has_been_visited = False


    def visit(self):
        """Set visited flag to true."""
        self.has_been_visited = True
        

    def set_description(self, message):
        """Replace the description with the given message."""
        self.description = message
        
        
    def add_note(self, *mids):
        """Add the given message IDs to the list of notes."""
        self.notes.extend(mids)
        
        
    def remove_note(self, *mids):
        """Remove all copies of each of the given notes from the list."""
        self.notes = [mid for mid in self.notes if mid not in mids]
        
        
    def clear_notes(self):
        self.notes = []
