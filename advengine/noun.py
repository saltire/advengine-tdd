class Noun:
    def __init__(self, ndata):
        self.description = ndata.get('desc', '')
        self.initial_locs = ndata.get('locs', [])
        self.is_movable = ndata.get('movable', False)
        self.is_visible = ndata.get('visible', False)
        self.is_wearable = ndata.get('wearable', False)
        self.name = ndata.get('name', '')
        self.notes = ndata.get('notes', [])
        self.shortdesc = ndata.get('shortdesc', '')
        self.shortname = ndata.get('shortname', '')
        self.words = set(ndata.get('words', []))


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
