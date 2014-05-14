from turn import Turn


class State:
    def __init__(self, data):
        self.nouns = data.nouns
        self.rooms = data.rooms
        self.vars = data.vars
        self.messages = data.messages
        self.lexicon = data.lexicon

        self.current_room = next(room for room in self.rooms.itervalues() if room.is_start)
        self.current_room.visit()

        # junction lists
        self.locations = set()
        self.tags = set()
        for noun in self.nouns.itervalues():
            self.locations |= set((noun, self.locations_by_id(lid)) for lid in noun.initial_locs)
            self.tags |= set((noun, tag) for tag in noun.initial_tags)
        for room in self.rooms.itervalues():
            self.tags |= set((room, tag) for tag in room.initial_tags)

        self.current_turn = None


    def start_turn(self, command):
        """Create a new turn object with the given command."""
        self.current_turn = Turn(command)


    def command_matches(self, control_str):
        """Check if the number of terms in the given control string is equal to or less
        than the number of words in current turn's command, and each term is a wildcard,
        a synonymous word, or a piped list of words where at least one is synonymous."""
        control_terms = [cterm for cterm in control_str.lower().split()
                         if cterm not in ('a', 'an', 'the')]
        return (len(control_terms) <= len(self.current_turn.words) and
                all(cterm == '*' or
                    any(self.lexicon.words_match(cword, self.current_turn.words[i])
                        for cword in cterm.split('|'))
                    for i, cterm in enumerate(control_terms)))


    def sub_words(self, phrase):
        return self.current_turn.sub_words(phrase) if self.current_turn is not None else phrase


    def locations_by_id(self, lid):
        """Return the noun or room with the given ID."""
        return (lid if lid in ('INVENTORY', 'WORN')
                else self.nouns.get(lid) or self.rooms.get(lid))


    def entities_by_tag(self, *tags):
        """Return a list of rooms or nouns with at least one of the given tags."""
        return set(entity for entity, tag in self.tags if tag in tags)


    def nouns_by_tag(self, *tags):
        """Return a list of nouns with at least one of the given tags."""
        return self.entities_by_tag(*tags) & set(self.nouns.itervalues())


    def rooms_by_tag(self, *tags):
        """Return a list of rooms with at least one of the given tags."""
        return self.entities_by_tag(*tags) & set(self.rooms.itervalues())


    def nouns_by_word(self, *words):
        """Return a list of nouns that match any of the given words."""
        return set(noun for noun in self.nouns.itervalues() if set(words) & noun.words)


    def nouns_by_input_word(self, wordnum):
        """Return a list of nouns matching the input word at the given index."""
        try:
            return self.nouns_by_word(self.current_turn.words[wordnum - 1])
        except IndexError:
            return set()


    def nouns_at_loc(self, *locs):
        """Return all nouns at any of the given locations."""
        return set(noun for noun, loc in self.locations if loc in locs)


    def noun_locs(self, *nouns):
        """Return all nouns or rooms containing any of the given nouns."""
        return set(loc for noun, loc in self.locations if noun in nouns)


    def add_noun(self, noun, *locs):
        """Add the given noun to all the given locations."""
        self.locations |= set((noun, loc) for loc in locs)


    def remove_noun(self, noun, *locs):
        """Remove the given noun from all the given locations."""
        self.locations -= set((noun, loc) for loc in locs)


    def move_noun(self, noun, *locs):
        """Replace the given noun's current locations with the given ones."""
        self.clear_noun_locs(noun)
        self.add_noun(noun, *locs)


    def clear_noun_locs(self, *nouns):
        """Remove the given nouns from all locations."""
        self.locations -= set((noun, loc) for noun, loc in self.locations if noun in nouns)


    def add_tag(self, tag, *entities):
        """Add the tag to all given entities."""
        self.tags |= set((entity, tag) for entity in entities)


    def remove_tag(self, tag, *entities):
        """Remove the tag from all given entities."""
        self.tags -= set((entity, tag) for entity in entities)
