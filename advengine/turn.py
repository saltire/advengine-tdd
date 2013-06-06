class Turn:
    def __init__(self, command):
        self.command = command
        self.words = [word for word in command.split()
                      if word not in ('a', 'an', 'the')]
        
    