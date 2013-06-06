from turn import Turn


class State:
    def __init__(self, data):
        self.nouns = data.nouns
        self.rooms = data.rooms
        self.vars = data.vars
        self.messages = data.messages
        self.lexicon = data.lexicon
        
        self.locations = set()
        for noun in self.nouns.values():
            self.locations |= set((noun, self.object_by_id(oid))
                                  for oid in noun.initial_locs())
            
        self.current_turn = None
            
            
    def start_turn(self, command):
        """Create a new turn object with the given command."""
        self.current_turn = Turn(command)
        
        
    def command_matches(self, command):
        """Check if the given command has the same number of words as the
        current turn's command, and each word is synonymous or a wildcard."""
        cwords = [cword for cword in command.lower().split()
                      if cword not in ('a', 'an', 'the')]
        return (len(cwords) == len(self.current_turn.words) and
                all(cword == '*' or
                    self.lexicon.words_match(cword, self.current_turn.words[i])
                    for i, cword in enumerate(cwords)))
                
            
    def object_by_id(self, oid):
        """Return the noun or room with the given ID."""
        return self.nouns.get(oid) or self.rooms.get(oid)
        
        
    def nouns_at_loc(self, t_obj):
        """Return all nouns at the given location."""
        return set(noun for noun, obj in self.locations if obj == t_obj)
    
    
    def noun_locs(self, t_noun):
        """Return all nouns or rooms containing the given noun."""
        return set(obj for noun, obj in self.locations if noun == t_noun)
    