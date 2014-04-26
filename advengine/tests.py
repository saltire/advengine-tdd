import random
import re

from selector import selector


class BaseTests:
    def __init__(self, state):
        self.state = state
        self.tests = self


    def command(self, *words):
        """Check if the given words match the current turn's command."""
        return (self.state.current_turn is not None and
                self.state.command_matches(' '.join(words)))


class Tests(BaseTests):

    @selector('entity')
    def any(self, entities):
        """Check if the selector matches at least one noun or room."""
        return any(entities)


    def var(self, var, value):
        """Check if the given variable is set to the given value."""
        match = re.match('([<>]?=*)-?(\d+)', str(value))
        if match is None:
            return False

        oper = '==' if match.group(1) in ('', '=') else match.group(1)
        return eval('self.state.vars[var]{0}{1}'.format(oper, match.group(2)))


    @selector('room')
    def room(self, rooms):
        """Check if any given room is the current room."""
        return self.state.current_room in rooms


    @selector('room')
    def visited(self, rooms):
        """Check if any given room has ever been visited."""
        return any(room.has_been_visited for room in rooms)


    def exitexists(self, direction):
        """Check if the current room has an exit in the given direction."""
        direction = self.state.sub_words(direction)
        return any(self.state.lexicon.words_match(direction, exdir)
                   for exdir in self.state.current_room.exits)


    @selector('noun', 'location')
    def nounloc(self, nouns, locs):
        """Check if any of the given nouns are at any of the given locations."""
        return bool(self.state.noun_locs(*nouns) & locs)


    @selector('noun')
    def carrying(self, nouns=None):
        """Check if any given noun is in the inventory,
        or if any noun at all is in the inventory if none specified."""
        if nouns is None:
            return bool(self.state.nouns_at_loc('INVENTORY'))
        return 'INVENTORY' in self.state.noun_locs(*nouns)


    @selector('noun')
    def wearing(self, nouns=None):
        """Check if any given noun is being worn,
        or if any noun at all is being worn if none specified."""
        if nouns is None:
            return bool(self.state.nouns_at_loc('WORN'))
        return 'WORN' in self.state.noun_locs(*nouns)


    @selector('noun')
    def inroom(self, nouns):
        """Check if any given noun is in the current room."""
        return self.state.current_room in self.state.noun_locs(*nouns)


    @selector('noun')
    def present(self, nouns):
        """Check if any given noun is in the current room, carried,
        worn, or inside another noun that is present."""
        def is_present(noun):
            return any(loc in (self.state.current_room, 'INVENTORY', 'WORN')
                       or (loc in self.state.nouns.itervalues() and is_present(loc))
                       for loc in self.state.noun_locs(noun))
        return any(is_present(noun) for noun in nouns)


    @selector('noun')
    def contained(self, nouns):
        """Check if any given noun is inside some other noun."""
        return any(loc in self.state.nouns.itervalues() for loc in self.state.noun_locs(*nouns))


    @selector('noun')
    def somewhere(self, nouns):
        """Check if any given noun has at least one location."""
        return bool(self.state.noun_locs(*nouns))


    @selector('noun')
    def movable(self, nouns):
        """Check if any given noun can be picked up or dropped."""
        return any(noun.is_movable for noun in nouns)


    @selector('noun')
    def wearable(self, nouns):
        """Check if any given noun can be worn."""
        return any(noun.is_wearable for noun in nouns)


    @selector('entity')
    def hasdesc(self, entities):
        """Check if any given noun or room has a description set."""
        return any(entity.description for entity in entities)


    @selector('entity')
    def hasnotes(self, entities):
        """Check if any given noun or room has any notes set."""
        return any(entity.notes for entity in entities)


    @selector('location')
    def hascontents(self, locs):
        """Check if any given location has nouns located inside it."""
        return bool(self.state.nouns_at_loc(*locs))


    def random(self, percent):
        """Return true a given percent of the time."""
        return random.random() * 100 < percent
