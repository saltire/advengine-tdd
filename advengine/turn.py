import re


class Turn:
    def __init__(self, command):
        self.command = command
        self.words = self._parse_words(command)


    def replace_command(self, command):
        """Replace the words with ones from a replacement command."""
        self.words = self._parse_words(self.sub_words(command))


    def _parse_words(self, command):
        """Split up the command into a list of words, excluding articles."""
        return [word for word in command.lower().split() if word not in ('a', 'an', 'the')]


    def sub_words(self, message):
        """Given a message, replace each numerical wildcard in the message
        with the word at that position in this turn's command."""
        def sub_word(match):
            wnum = int(match.group(1)) - 1
            return self.words[wnum] if len(self.words) > wnum else ''

        return re.sub('%(\d+)', sub_word, message)
