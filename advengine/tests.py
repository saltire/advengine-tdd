class Tests:
    def __init__(self, state):
        self.state = state
        
        
    def command(self, *words):
        return self.state.command_matches(' '.join(words))
        
        
    def var(self, var, value):
        return self.state.vars.get(var) == int(value)