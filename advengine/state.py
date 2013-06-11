from turn import Turn


class State:
    def __init__(self, data):
        self.nouns = data.nouns
        self.rooms = data.rooms
        self.vars = data.vars
        self.messages = data.messages
        self.lexicon = data.lexicon
        
        self.current_room = next(room for room in self.rooms.values()
                                 if room.is_start)
        self.current_room.visit()
        
        # a junction list of nouns and locations
        self.locations = set()
        for noun in self.nouns.values():
            self.locations |= set((noun, self.locations_by_id(lid))
                                  for lid in noun.initial_locs())
            
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
                
            
    def locations_by_id(self, lid):
        """Return the noun or room with the given ID."""
        return (lid if lid in ('INVENTORY', 'WORN') else
                self.nouns.get(lid) or self.rooms.get(lid))
        
        
    def nouns_by_word(self, *words):
        """Return a list of nouns that match the given word."""
        return set(noun for noun in self.nouns.values() if set(words) & noun.words)
    
    
    def nouns_by_input_word(self, wordnum):
        """Return a list of nouns matching the input word at the given index."""
        try:
            return self.nouns_by_word(self.current_turn.words[wordnum - 1])
        except IndexError:
            return set()
        
        
    def nouns_at_loc(self, *locs):
        """Return all nouns at the given location."""
        return set(noun for noun, loc in self.locations if loc in locs)
    
    
    def noun_locs(self, *nouns):
        """Return all nouns or rooms containing the given noun."""
        return set(obj for noun, obj in self.locations if noun in nouns)
    