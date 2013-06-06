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
        self.current_turn = Turn(command)
        
        
    def command_matches(self, command):
        cwords = [cword for cword in command.split()
                      if cword not in ('a', 'an', 'the')]
        return (len(cwords) == len(self.current_turn.words) and
                all(self.lexicon.words_match(word, cwords[i])
                    for i, word in enumerate(self.current_turn.words)))
                
            
    def object_by_id(self, oid):
        return self.nouns.get(oid) or self.rooms.get(oid)
        
        
    def nouns_at_loc(self, t_obj):
        return set(noun for noun, obj in self.locations if obj == t_obj)
    
    
    def noun_locs(self, t_noun):
        return set(obj for noun, obj in self.locations if noun == t_noun)
    