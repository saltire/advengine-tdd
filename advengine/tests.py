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


