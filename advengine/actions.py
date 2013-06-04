class Actions:
    def __init__(self, state):
        self.state = state
        
        
    def message(self, mid):
        return [self.state.messages.get(mid, '')]