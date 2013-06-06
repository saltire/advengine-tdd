import re


class Actions:
    def __init__(self, state):
        self.state = state
        
        
    def message(self, mid):
        """Send the message matching the given ID."""
        def sub_words(match):
            wnum = int(match.group(1)) - 1
            return (self.state.current_turn.words[wnum]
                    if len(self.state.current_turn.words) > wnum
                    else '')
            
        return [re.sub('%(\d+)', sub_words, self.state.messages.get(mid, ''))]

