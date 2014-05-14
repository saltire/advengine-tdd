class Room:
    def __init__(self, rdata):
        self.description = rdata.get('desc', '')
        self.exits = rdata.get('exits', {})
        self.has_been_visited = False
        self.is_start = rdata.get('start') is True
        self.name = rdata.get('name', '')
        self.notes = rdata.get('notes', [])
        self.tags = set(rdata.get('tags', []))


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
