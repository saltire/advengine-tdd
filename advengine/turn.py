class Turn:
    def __init__(self, command):
        self.command = command
        self.words = [word for word in command.lower().split()
                      if word not in ('a', 'an', 'the')]
        
    