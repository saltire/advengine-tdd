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