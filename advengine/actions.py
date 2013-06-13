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


    @selector('object')
    def showdesc(self, objects):
        """Return the descriptions of each object passed."""
        return [obj.description for obj in objects if obj.description]
    
    
    @selector('object')
    def shownotes(self, objects):
        """Return a list of all notes of each object passed."""
        return reduce(lambda x, y: x + y,
                      ([self.state.messages[mid] for mid in obj.notes]
                       for obj in objects))


    def move(self, direction):
        """If the current room has an exit in the given direction, move to
        the room at that exit."""
        try:
            self.state.current_room = self.state.rooms[
                self.state.current_room.exits[direction]]
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