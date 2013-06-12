import random

from filters import noun_filter, noun_location_filter


class Tests:
    def __init__(self, state):
        self.state = state
        
        
    def command(self, *words):
        """Check if the given words match the current turn's command."""
        return (self.state.current_turn is not None and
                self.state.command_matches(' '.join(words)))
        
        
    def var(self, var, value):
        """Check if the given variable is set to the given value."""
        return self.state.vars.get(var) == int(value)
    
    
    def room(self, rid):
        """Check if the given room is the current room."""
        return self.state.current_room == self.state.rooms[rid]
    
    
    def visited(self, rid):
        """Check if the given room has ever been visited."""
        return self.state.rooms[rid].has_been_visited
    
    
    def exitexists(self, direction):
        """Check if the current room has an exit in the given direction."""
        return direction in self.state.current_room.exits
    
    
    @noun_filter
    def carrying(self, nouns):
        """Check if any of the given nouns are in the inventory."""
        return 'INVENTORY' in self.state.noun_locs(*nouns)
    
    
    @noun_location_filter
    def nounloc(self, nouns, locs):
        """Check if any of the given nouns are at any of the given locations."""
        return bool(self.state.noun_locs(*nouns) & locs)
        
    
    @noun_filter
    def ininv(self, nouns):
        """Check if any given noun is in the inventory."""
        return 'INVENTORY' in self.state.noun_locs(*nouns)


    @noun_filter
    def worn(self, nouns):
        """Check if any given noun is in the inventory."""
        return 'WORN' in self.state.noun_locs(*nouns)
    
    
    @noun_filter
    def inroom(self, nouns):
        """Check if any given noun is in the current room."""
        return self.state.current_room in self.state.noun_locs(*nouns)


    @noun_filter
    def present(self, nouns):
        """Check if any given noun is in the current room, carried, worn,
        or inside another noun that is present."""
        def is_present(noun):
            return any(loc in (self.state.current_room, 'INVENTORY', 'WORN')
                       or (loc in self.state.nouns.values() and is_present(loc))
                       for loc in self.state.noun_locs(noun))
        return any(is_present(noun) for noun in nouns)
    
    
    @noun_filter
    def contained(self, nouns):
        """Check if any given noun is inside some other noun."""
        return any(loc in self.state.nouns.values()
                   for loc in self.state.noun_locs(*nouns))
        
        
    @noun_filter
    def somewhere(self, nouns):
        """Check if any given noun has at least one location."""
        return bool(self.state.noun_locs(*nouns))
    
    
    @noun_filter
    def movable(self, nouns):
        """Check if any given noun can be picked up or dropped."""
        return any(noun.is_movable for noun in nouns)
    
    
    @noun_filter
    def wearable(self, nouns):
        """Check if any given noun can be picked up or dropped."""
        return any(noun.is_wearable for noun in nouns)
    
    
    @noun_filter
    def hasdesc(self, nouns):
        """Check if any given noun has a description set."""
        return any(noun.description for noun in nouns)
    
    
    @noun_filter
    def hasnotes(self, nouns):
        """Check if any given noun has any notes set."""
        return any(noun.notes for noun in nouns)
    
    
    @noun_filter
    def hascontents(self, nouns):
        """Check if any given noun has other nouns located inside it."""
        return bool(self.state.nouns_at_loc(*nouns))
    
    
    def random(self, percent):
        """Return true a given percent of the time."""
        return random.random() * 100 < percent
    
