import re


class Tests:
    def __init__(self, state):
        self.state = state
        
        
    def _filter_nouns(self, nfilter):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the filter as a pipe-
        delimited list of noun IDs and return those nouns."""
        if re.match('%(\d+)', nfilter) is not None:
            return self.state.nouns_by_input_word(int(nfilter[1:]))
        else:
            return [self.state.nouns[nid] for nid in nfilter.split('|')]
        
        
    def _filter_locations(self, lfilter):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the filter as a pipe-
        delimited list of location IDs and return those locations."""
        if re.match('%(\d+)', lfilter) is not None:
            return self.state.nouns_by_input_word(int(lfilter[1:]))
        else:
            return [self.state.locations_by_id(lid)
                    for lid in lfilter.split('|')]
        
        
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
    
    
    def carrying(self, nfilter):
        """Check if any of the given nouns are in the inventory."""
        return 'INVENTORY' in self.state.noun_locs(*self._filter_nouns(nfilter))
    
    
    def nounloc(self, nfilter, lfilter):
        """Check if any of the given nouns are at any of the given locations."""
        return bool(self.state.noun_locs(*self._filter_nouns(nfilter)) &
                    self._filter_locations(lfilter))