class Turn:
    def __init__(self, command):
        self.command = command
        self.words = self._parse_words(command)
        
    
    def replace_command(self, command):
        """Replace the words with ones from a replacement command."""
        self.words = self._parse_words(command)
        
        
    def _parse_words(self, command):
        """Split up the command into a list of words, excluding articles."""
        return [word for word in command.lower().split()
                if word not in ('a', 'an', 'the')]
