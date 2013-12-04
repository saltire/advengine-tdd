from selector import selector
from tests import BaseTests


class BaseActions:
    def __init__(self, state, tests=None):
        self.state = state
        self.tests = tests or BaseTests(state)


class Actions(BaseActions):
    def message(self, *mids):
        """Return the messages matching the given IDs,
        substituting numerical wildcards if necessary."""
        return [self.state.sub_words(self.state.messages[mid]) for mid in mids]


    def pause(self):
        """Return a symbol indicating that the game should pause and
        wait for the player to press a key."""
        return 'PAUSE'


    @selector('entity')
    def showdesc(self, entities=None):
        """Return the descriptions of each entity passed.
        If no entity is passed, return the description of the current room."""
        entities = entities if entities is not None else [self.state.current_room]
        return [entity.description for entity in entities if entity.description]


    @selector('entity')
    def shownotes(self, entities=None):
        """Return a list of all notes of each entity passed.
        If no entity is passed, return the notes for the current room."""
        entities = entities if entities is not None else [self.state.current_room]
        return [self.state.messages[mid] for entity in entities for mid in entity.notes]


    @selector('location')
    def showcontents(self, locs=None, text='name', noun_msg=None, in_msg=None, worn_msg=None,
                     recursive=False, indent=False, contains_msg=None):
        """Return a listing of all nouns at the given location.
        If no location is passed, use the current room.
        Contains a subfunction that can be executed recursively."""
        locs = locs if locs is not None else [self.state.current_room]

        def list_contents(locs, level=0):
            items = []
            for noun in self.state.nouns_at_loc(*locs):
                if noun.is_visible:
                    name = getattr(noun, text)
                    if noun_msg:
                        # use a message instead of the plain name
                        name = self.state.messages[noun_msg].replace('%NOUN', name)
                    if indent and level > 0:
                        # indent the item to show that it is contained in another noun
                        name = '\t' * level + name
                    if in_msg and level > 0:
                        # add a note naming this item's containing noun
                        name += self.state.messages[in_msg].replace('%NOUN', locs[0].shortname)
                    if worn_msg and 'WORN' in self.state.noun_locs(noun):
                        # add a note that this item is being worn
                        name += self.state.messages[worn_msg]
                    items.append(name)

                    if recursive and self.state.nouns_at_loc(noun):
                        if contains_msg:
                            items.append(self.state.messages[contains_msg]
                                         .replace('%NOUN', noun.shortname))
                        # also list all the items contained in this noun
                        items.extend(list_contents([noun], level + 1))

            return items

        contents = list_contents(locs)
        return '\n'.join(contents) if contents else None


    def inv(self, text='name', noun_msg=None, in_msg=None, worn_msg=None,
            recursive=False, indent=False, contains_msg=None):
        """Return a listing of all nouns that are in the inventory
        or being worn."""
        return self.showcontents('INVENTORY|WORN', text, noun_msg, in_msg, worn_msg,
                                 recursive, indent, contains_msg)


    def move(self, direction):
        """If the current room has an exit in the given direction,
        move to the room at that exit."""
        direction = self.state.sub_words(direction)
        try:
            self.state.current_room = next(self.state.rooms[rid] for exdir, rid
                                           in self.state.current_room.exits.iteritems()
                                           if self.state.lexicon.words_match(direction, exdir))
        except StopIteration:
            pass


    @selector('noun')
    def destroy(self, nouns):
        """Remove the given nouns from all locations."""
        self.state.clear_noun_locs(*nouns)


    @selector('noun', 'location')
    def sendnoun(self, nouns, locs):
        """Move the given nouns to the given locations."""
        for noun in nouns:
            self.state.move_noun(noun, *locs)


    @selector('noun')
    def sendtoroom(self, nouns):
        """Move the given nouns to the current room."""
        for noun in nouns:
            self.state.move_noun(noun, self.state.current_room)


    @selector('noun')
    def sendtoinv(self, nouns):
        """Move the given nouns to the inventory."""
        for noun in nouns:
            self.state.move_noun(noun, 'INVENTORY')


    @selector('noun')
    def wear(self, nouns):
        """Move the given nouns to the list of items worn."""
        for noun in nouns:
            self.state.move_noun(noun, 'WORN')


    @selector('noun', 'noun')
    def sendtonounloc(self, s_nouns, d_nouns):
        """Move the given source nouns to the locations of the given
        destination nouns."""
        locs = self.state.noun_locs(*d_nouns)
        for noun in s_nouns:
            self.state.move_noun(noun, *locs)


    @selector('noun', 'noun')
    def sendtonoun(self, s_nouns, d_nouns):
        """Move the given source nouns into the given destination nouns."""
        for noun in s_nouns:
            self.state.move_noun(noun, *d_nouns)


    @selector('noun', 'noun')
    def swapnouns(self, nouns1, nouns2):
        """Move the first given nouns to the location of the second
        given nouns, and vice versa."""
        locs1 = self.state.noun_locs(*nouns1)
        locs2 = self.state.noun_locs(*nouns2)
        for noun in nouns1:
            self.state.move_noun(noun, *locs2)
        for noun in nouns2:
            self.state.move_noun(noun, *locs1)


    @selector('noun')
    def setnoundesc(self, nouns, mid):
        """Set the description for the given nouns to the message with
        the given ID."""
        for noun in nouns:
            noun.set_description(self.state.messages[mid])


    @selector('noun')
    def addnounnote(self, nouns, *mids):
        """Add the given message IDs to the notes for each given noun."""
        for noun in nouns:
            noun.add_note(*mids)


    @selector('noun')
    def removenounnote(self, nouns, *mids):
        """Remove all the given message IDs from notes for each given noun."""
        for noun in nouns:
            noun.remove_note(*mids)


    @selector('noun')
    def clearnounnotes(self, nouns):
        """Clear the notes for each given noun."""
        for noun in nouns:
            noun.clear_notes()


    @selector('room')
    def setroomdesc(self, rooms, mid):
        """Set the description for the given rooms to the message with
        the given ID."""
        for room in rooms:
            room.set_description(self.state.messages[mid])


    @selector('room')
    def addroomnote(self, rooms, *mids):
        """Add the given message IDs to the notes for each given room."""
        for room in rooms:
            room.add_note(*mids)


    @selector('room')
    def removeroomnote(self, rooms, *mids):
        """Remove all the given message IDs from notes for each given room."""
        for room in rooms:
            room.remove_note(*mids)


    @selector('room')
    def clearroomnotes(self, rooms):
        """Clear the notes for each given room."""
        for room in rooms:
            room.clear_notes()


    def setvar(self, var, value):
        """Set the given variable to the given integer value."""
        self.state.vars[var] = int(value)


    def adjustvar(self, var, value):
        """Add, subtract, multiply, or divide the given variable
        depending on the given integer value and any arithmetic
        operators preceding it."""
        try:
            self.state.vars[var] += value

        except TypeError:
            if value[0] == '-':
                self.state.vars[var] -= int(value[1:])

            elif value[0] in ('*', 'x'):
                self.state.vars[var] *= int(value[1:])

            elif value[0] == '/':
                self.state.vars[var] /= int(value[1:])

            elif value[0] == '+' or value.isdigit():
                self.state.vars[var] += int(value.lstrip('+'))
