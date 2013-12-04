import itertools

from actions import Actions
from gamedata import GameData
from state import State
from tests import Tests


class Adventure:
    def __init__(self, gamedata, testclass=Tests, actionclass=Actions):
        data = GameData(gamedata)
        self.controls = data.controls

        self.state = State(data)
        self.tests = testclass(self.state)
        self.actions = actionclass(self.state, self.tests)

        self.game_over = False


    def start_game(self):
        """Run any actions that occur before the first turn."""
        return self.do_actions(self.controls.get('before_game', []))


    def do_command(self, command):
        """Start a new turn with the given command, run any actions,
        and return any resulting messages. End the game if the gameover
        flag has been set."""
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
        actions = itertools.chain(*[control.get_actions(self.tests) for control in controls])
        messages = []

        for action, args in actions:
            if action == 'done':
                # end execution of actions
                break
            elif action == 'gameover':
                # end execution of actions and end the game
                self.game_over = True
                break
            elif action == 'replace':
                # replace the input command and restart execution
                self.state.current_turn.replace_command(' '.join(args))
                return self.do_actions(controls)

            # treat name=value args as keyword args
            pargs, kwargs = [], {}
            for arg in args:
                if '=' in arg:
                    kwargs.update([arg.split('=', 1)])
                else:
                    pargs.append(arg)

            msgs = getattr(self.actions, action)(*pargs, **kwargs)
            if isinstance(msgs, basestring):
                messages.append(msgs)
            elif msgs is not None:
                messages.extend(msgs)

        return messages
