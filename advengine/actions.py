import re

from selector import selector


class Actions:
    def __init__(self, state):
        self.state = state


    def message(self, *mids):
        """Return the messages matching the given IDs."""
        def sub_words(match):
            wnum = int(match.group(1)) - 1
            return (self.state.current_turn.words[wnum]
                    if len(self.state.current_turn.words) > wnum
                    else '')

        return [re.sub('%(\d+)', sub_words, self.state.messages[mid])
                for mid in mids]


    def pause(self):
        """Return a symbol indicating that the game should pause and
        wait for the player to press a key."""
        return 'PAUSE'


    @selector('entity')
    def showdesc(self, entities):
        """Return the descriptions of each object passed."""
        return [entity.description for entity in entities if entity.description]


    @selector('entity')
    def shownotes(self, entities):
        """Return a list of all notes of each object passed."""
        return [self.state.messages[mid]
                for entity in entities for mid in entity.notes]


    @selector('location')
    def showcontents(self, locs, text='name', recursive=False, indent=False, in_msg=None,
                     worn_msg=None):
        """Return a listing of all nouns at the given location.
        Contains a subfunction that can be executed recursively."""

        def list_contents(locs):
            # for each item at this location, return its name
            # if listing recursively, return each of the items inside
            #     and optionally a message naming the immediate container of each
            items = []
            for noun in self.state.nouns_at_loc(*locs):
                # get the string for the noun
                # optionally add a note if the item is being worn
                name = (getattr(noun, text)
                        + (self.state.messages[worn_msg] if 'WORN' in self.state.noun_locs(noun)
                           and worn_msg else ''))
                items.append((name, ''))

                if recursive:
                    # message to add to any contained items, with the name of the container
                    # only add this if the item doesn't already have one from a subcontainer
                    item_in_msg = (self.state.messages[in_msg].replace('%NOUN', noun.shortname)
                                   if in_msg else '')

                    # add contained nouns to listing, with an indent if specified
                    for subitem, subitem_in_msg in list_contents([noun]):
                        items.append((('\t' if indent else '') + subitem,
                                     subitem_in_msg or item_in_msg))
            return items

        # join each item with its container message, then join them all as separate lines
        return '\n'.join(''.join(item) for item in list_contents(locs))


    def move(self, direction):
        """If the current room has an exit in the given direction,
        move to the room at that exit."""
        try:
            self.state.current_room = self.state.rooms[self.state.current_room.exits[direction]]
        except KeyError:
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
