from actions import Actions
from gamedata import GameData
from state import State
from tests import Tests


class Adventure:
    def __init__(self, gamedata):
        data = GameData(gamedata)
        self.controls = data.controls
        
        self.state = State(data)
        self.tests = Tests(self.state)
        self.actions = Actions(self.state)
    
    
    def start_game(self):
        """Run any actions that occur before the first turn."""
        return self.do_actions(self.controls['before_game'])
    
    
    def do_command(self, command):
        """Start a new turn with the given command, run any actions,
        and return any resulting messages."""
        self.state.start_turn(command)
        return (self.do_actions(self.controls['before_turn']) +
                self.do_actions(self.controls['during_turn']) +
                self.do_actions(self.controls['after_turn']))
        
        
    def do_actions(self, controls):
        """Evaluate each of the controls, run any actions and return
        any messages."""
        actions = []
        for control in controls:
            actions.extend(control.get_actions(self.tests))
            
        messages = []
        for action, args in actions:
            msgs = getattr(self.actions, action)(*args)
            if msgs is not None:
                messages.extend(msgs)
        
        return messages
