class Tests:
    def __init__(self, state):
        self.state = state
        
        
    def var(self, var, value):
        return self.state.vars.get(var) == int(value)