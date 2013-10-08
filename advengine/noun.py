class Noun:
    def __init__(self, ndata):
        self.data = ndata

        self.description = self.data.get('desc', '')
        self.is_movable = self.data.get('movable', False)
        self.is_visible = self.data.get('visible', False)
        self.is_wearable = self.data.get('wearable', False)
        self.name = self.data.get('name', '')
        self.notes = self.data.get('notes', [])
        self.shortdesc = self.data.get('shortdesc', '')
        self.shortname = self.data.get('shortname', '')
        self.words = set(self.data.get('words', []))


    def initial_locs(self):
        """Return the IDs of all nouns or rooms containing the noun
        at the start of the game."""
        return self.data.get('locs', [])


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
