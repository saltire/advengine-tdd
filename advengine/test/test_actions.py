import unittest

from advengine.actions import Actions
from advengine.gamedata import GameData
from advengine.state import State


class Test_Actions(unittest.TestCase):
    def setUp(self):
        data = GameData({'rooms': {'start': {'start': True,
                                             'desc': 'The starting room.'}},
                         'nouns': {'window': {'desc': 'Made of glass.'},
                                   'table': {}
                                   },
                         'vars': {'one': 1, 'two': 2},
                         'messages': {'pass': 'Pass',
                                      'subword': "Second word is %2"
                                      }
                         })
        self.state = State(data)
        self.actions = Actions(self.state)


    def test_message(self):
        self.assertEqual(self.actions.message('pass'), ['Pass'])
        

    def test_message_replaces_numerical_wildcard(self):
        self.state.start_turn('testing numbered words')
        self.assertEqual(self.actions.message('subword'),
                         ['Second word is numbered'])
        
        
    def test_pause(self):
        pass
    
    
    def test_showdesc(self):
        self.assertEqual(self.actions.showdesc('start'), ['The starting room.'])
        self.assertEqual(self.actions.showdesc('window'), ['Made of glass.'])
        self.assertEqual(self.actions.showdesc('table'), [])
    
    
    def test_shownotes(self):
        pass
    
    
    def test_showcontents(self):
        pass
    
    
    def test_listcontents(self):
        pass
    
    
    def test_inv(self):
        pass
    
    
    def test_move(self):
        pass
    
    
    def test_destroy(self):
        pass
    
    
    def test_sendnoun(self):
        pass
    
    
    def test_sendtoroom(self):
        pass
    
    
    def test_sendtoinv(self):
        pass
    
    
    def test_wear(self):
        pass
    
    
    def test_sendtonounloc(self):
        pass
    
    
    def test_sendtonoun(self):
        pass
    
    
    def test_swapnouns(self):
        pass
    
    
    def test_setnoundesc(self):
        pass
    
    
    def test_addnounnote(self):
        pass
    
    
    def test_removenounnote(self):
        pass
    
    
    def test_clearnounnotes(self):
        pass
    
    
    def test_setroomdesc(self):
        pass
    
    
    def test_addroomnote(self):
        pass
    
    
    def test_removeroomnote(self):
        pass
    
    
    def test_clearroomnotes(self):
        pass
    
    
    def test_setvar(self):
        pass
    
    
    def test_adjustvar(self):
        pass
    
    
