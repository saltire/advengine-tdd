class Actions:
    def __init__(self, state):
        self.state = state
        
        
    def message(self, mid):
        """Send the message matching the given ID."""
        return [self.state.messages.get(mid, '')]