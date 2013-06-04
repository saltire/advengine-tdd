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
        actions = self.get_actions(self.controls['before_game'])
        return self.do_actions(actions)
    
    
    def do_command(self, command):
        actions = (self.get_actions(self.controls['before_turn']) +
                   self.get_actions(self.controls['during_turn']) +
                   self.get_actions(self.controls['after_turn']))
        
        return self.do_actions(actions)
        
        
    def get_actions(self, controls):
        actions = []
        
        for control in controls:
            actions.extend(control.get_actions(self.tests))
            
        return actions
    
    
    def do_actions(self, actions):
        messages = []
        
        for action, args in actions:
            msgs = getattr(self.actions, action)(*args)
            if msgs is not None:
                messages.extend(msgs)
        
        return messages