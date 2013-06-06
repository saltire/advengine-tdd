import unittest

from advengine.control import Control
from advengine.gamedata import GameData
from advengine.state import State
from advengine.tests import Tests


class Test_Control(unittest.TestCase):
    def setUp(self):
        data = GameData({'vars': {'one': 1, 'two': 2},
                         'messages': {'pass': 'Pass'}
                         })
        state = State(data)
        self.tests = Tests(state)
        
    
    def test_control_returns_actions_when_initialized_from_string(self):
        control = Control('message pass')
        self.assertItemsEqual(control.get_actions(self.tests),
                              [('message', ['pass'])])
       
       
    def test_control_returns_actions_when_if_is_string(self):
        cdata = {'if': 'var one 1',
                 'then': 'message pass'}
        control = Control(cdata)
        self.assertItemsEqual(control.get_actions(self.tests),
                              [('message', ['pass'])])
        
        
    def test_control_returns_actions_when_if_is_list_of_true(self):
        cdata = {'if': ['var one 1', 'var two 2'],
                 'then': 'message pass'}
        control = Control(cdata)
        self.assertItemsEqual(control.get_actions(self.tests),
                              [('message', ['pass'])])
        
        
    def test_control_doesnt_return_actions_when_if_is_list_with_false(self):
        cdata = {'if': ['var one 1', 'var two 1'],
                 'then': 'message pass'}
        control = Control(cdata)
        self.assertItemsEqual(control.get_actions(self.tests), [])
        
        
    def test_control_raises_type_error_when_not_passed_string_or_dict(self):
        self.assertRaises(TypeError, Control, ['action', 'action'])
    