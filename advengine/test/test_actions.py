import unittest

from advengine.actions import Actions
from advengine.gamedata import GameData
from advengine.state import State


class Test_Actions(unittest.TestCase):
    def setUp(self):
        data = GameData({'rooms': {'start': {'start': True,
                                             'desc': 'The starting room.',
                                              'notes': ['pass', 'fail'],
                                              'exits': {'south': 'finish'}},
                                   'finish': {}
                                   },
                         'nouns': {'window': {'desc': 'Made of glass.',
                                              'notes': ['pass', 'fail'],
                                              'locs': ['start', 'finish']},
                                   'hat': {'locs': ['finish']},
                                   'unicorn': {}
                                   },
                         'vars': {'one': 1, 'two': 2},
                         'messages': {'pass': 'Pass',
                                      'fail': 'Fail',
                                      'subword': "Second word is %2"
                                      }
                         })
        self.state = State(data)
        self.actions = Actions(self.state)

        for rid, room in self.state.rooms.items():
            setattr(self, rid, room)
        for nid, noun in self.state.nouns.items():
            setattr(self, nid, noun)


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
        self.assertEqual(self.actions.showdesc('unicorn'), [])


    def test_shownotes(self):
        self.assertEqual(self.actions.shownotes('start|window'),
                              ['Pass', 'Fail', 'Pass', 'Fail'])


    def test_showcontents(self):
        pass


    def test_listcontents(self):
        pass


    def test_inv(self):
        pass


    def test_move(self):
        self.actions.move('south')
        self.assertEqual(self.state.current_room, self.finish)


    def test_move_does_not_happen_without_matching_exit(self):
        self.actions.move('north')
        self.assertEqual(self.state.current_room, self.start)


    def test_destroy(self):
        self.actions.destroy('window')
        self.assertItemsEqual(self.state.noun_locs(self.window),
                              [])


    def test_sendnoun(self):
        self.actions.sendnoun('hat', 'start')
        self.assertItemsEqual(self.state.noun_locs(self.hat), [self.start])


    def test_sendtoroom(self):
        self.actions.sendtoroom('hat')
        self.assertItemsEqual(self.state.noun_locs(self.hat), [self.start])


    def test_sendtoinv(self):
        self.actions.sendtoinv('hat')
        self.assertItemsEqual(self.state.noun_locs(self.hat), ['INVENTORY'])


    def test_wear(self):
        self.actions.wear('hat')
        self.assertItemsEqual(self.state.noun_locs(self.hat), ['WORN'])


    def test_sendtonounloc(self):
        self.actions.sendtonounloc('unicorn', 'hat')
        self.assertItemsEqual(self.state.noun_locs(self.unicorn), [self.finish])


    def test_sendtonounloc_works_for_dest_nouns_in_multiple_locations(self):
        self.actions.sendtonounloc('unicorn', 'window')
        self.assertItemsEqual(self.state.noun_locs(self.unicorn),
                              [self.start, self.finish])


    def test_sendtonoun(self):
        self.actions.sendtonoun('unicorn', 'hat')
        self.assertItemsEqual(self.state.noun_locs(self.unicorn), [self.hat])


    def test_swapnouns(self):
        self.actions.swapnouns('hat', 'window')
        self.assertItemsEqual(self.state.noun_locs(self.hat),
                              [self.start, self.finish])
        self.assertItemsEqual(self.state.noun_locs(self.window),
                              [self.finish])


    def test_setnoundesc(self):
        self.actions.setnoundesc('hat', 'pass')
        self.assertEqual(self.hat.description, 'Pass')


    def test_addnounnote(self):
        self.actions.addnounnote('hat', 'pass')
        self.assertEqual(self.hat.notes, ['pass'])


    def test_addnounnote_with_multiple_notes(self):
        self.actions.addnounnote('hat', 'pass', 'fail')
        self.assertEqual(self.hat.notes, ['pass', 'fail'])


    def test_removenounnote(self):
        self.actions.removenounnote('window', 'pass')
        self.assertEqual(self.window.notes, ['fail'])


    def test_clearnounnotes(self):
        self.actions.clearnounnotes('window')
        self.assertEqual(self.window.notes, [])


    def test_setroomdesc(self):
        self.actions.setroomdesc('start', 'pass')
        self.assertEqual(self.start.description, 'Pass')


    def test_addroomnote(self):
        self.actions.addroomnote('start', 'pass')
        self.assertEqual(self.start.notes, ['pass', 'fail', 'pass'])


    def test_addroomnote_with_multiple_notes(self):
        self.actions.addroomnote('start', 'pass', 'fail')
        self.assertEqual(self.start.notes, ['pass', 'fail', 'pass', 'fail'])


    def test_removeroomnote(self):
        self.actions.removeroomnote('start', 'pass')
        self.assertEqual(self.start.notes, ['fail'])


    def test_clearroomnotes(self):
        self.actions.clearroomnotes('start')
        self.assertEqual(self.start.notes, [])


    def test_setvar_on_existing_variable(self):
        self.actions.setvar('one', 100)
        self.assertEqual(self.state.vars['one'], 100)


    def test_setvar_on_nonexisting_variable(self):
        self.actions.setvar('ten', 10)
        self.assertEqual(self.state.vars['ten'], 10)


    def test_setvar_casts_string_value_to_int(self):
        self.actions.setvar('one', '100')
        self.assertEqual(self.state.vars['one'], 100)


    def test_adjustvar_with_integer_adds(self):
        self.actions.adjustvar('one', 2)
        self.assertEqual(self.state.vars['one'], 3)


    def test_adjustvar_with_string_and_no_operator_adds(self):
        self.actions.adjustvar('two', '2')
        self.assertEqual(self.state.vars['two'], 4)


    def test_adjustvar_with_plus_adds(self):
        self.actions.adjustvar('one', '+2')
        self.assertEqual(self.state.vars['one'], 3)


    def test_adjustvar_with_minus_subtracts(self):
        self.actions.adjustvar('one', '-2')
        self.assertEqual(self.state.vars['one'], -1)


    def test_adjustvar_with_x_multiplies(self):
        self.actions.adjustvar('two', 'x2')
        self.assertEqual(self.state.vars['two'], 4)


    def test_adjustvar_with_slash_divides(self):
        self.actions.adjustvar('two', '/2')
        self.assertEqual(self.state.vars['two'], 1)
