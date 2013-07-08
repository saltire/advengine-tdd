import itertools

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
        
        self.game_over = False
        
        self.start_game()
    
    
    def start_game(self):
        """Run any actions that occur before the first turn."""
        return self.do_actions(self.controls.get('before_game', []))
    
    
    def do_command(self, command):
        """Start a new turn with the given command, run any actions,
        and return any resulting messages. End the game if the game over flag
        has been set."""
        self.state.start_turn(command)
        messages = []        
        
        for stage in ('before_turn', 'during_turn', 'after_turn'):
            messages += self.do_actions(self.controls.get(stage, []))
            
            if self.game_over:
                messages += self.do_actions(self.controls.get('after_game', []))
                break

        return messages
    
    
    def do_actions(self, controls):
        """Evaluate each of the controls, run any actions and return
        any messages. End execution if 'done', end game if 'gameover'."""
        actions = itertools.chain(*(control.get_actions(self.tests)
                                    for control in controls))
        messages = []

        for action, args in actions:
            if action == 'done':
                break
            elif action == 'gameover':
                self.game_over = True
                break
            elif action == 'replace':
                self.state.current_turn.replace_command(' '.join(args))
                return self.do_actions(controls)
            
            msgs = getattr(self.actions, action)(*args)
            if msgs is not None:
                messages.extend(msgs)

        return messages
