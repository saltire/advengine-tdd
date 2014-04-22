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


    def get_control_actions(self, control):
        """Run each set of tests for this control, and if all tests are true
        for any set of tests, return the 'then' actions, otherwise 'else'."""
        def test_is_true(test):
            # return opposite if test is preceded by a bang
            neg, test = (True, test[1:]) if test[0] == '!' else (False, test)

            method, args = test.split()[0], test.split()[1:]
            return getattr(self.tests, method)(*args) ^ neg

        results = (control['true_results'] if not control['conds']
                   or any(all(test_is_true(test) for test in cond) for cond in control['conds'])
                   else control['false_results'])

        actions = []

        for result in results:
            if isinstance(result, dict):
                # run tests for this control and return its actions
                actions.extend(self.get_control_actions(control))
            else:
                # return the actions
                action, args = result.split()[0], result.split()[1:]
                actions.append((action, args))

        return actions


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
