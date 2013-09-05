import unittest

from advengine.actions import Actions
from advengine.gamedata import GameData
from advengine.state import State


class Test_Actions(unittest.TestCase):
    def setUp(self):
        data = GameData({'rooms': {'start': {'start': True,
                                             'desc': 'The starting room.',
                                             'notes': ['pass', 'fail'],
                                             'exits': {'south': 'finish'},
                                             },
                                   'finish': {},
                                   },
                         'nouns': {'window': {'name': 'A window.',
                                              'shortname': 'window',
                                              'shortdesc': 'You see a window.',
                                              'desc': 'Made of glass.',
                                              'notes': ['pass', 'fail'],
                                              'locs': ['start', 'finish'],
                                              },
                                   'bowl': {'name': 'A bowl.',
                                            'shortname': 'bowl',
                                            'shortdesc': 'A bowl is here.',
                                            'desc': 'The bowl is red.',
                                            'locs': ['finish'],
                                            },
                                   'apple': {'name': 'An apple.',
                                             'shortname': 'apple',
                                             'locs': ['bowl'],
                                             },
                                   'worm': {'name': 'A worm.', 'locs': ['apple']},
                                   'money': {'name': 'Some money.', 'locs': ['INVENTORY']},
                                   'unicorn': {},
                                   },
                         'vars': {'one': 1, 'two': 2},
                         'messages': {'pass': 'Pass',
                                      'fail': 'Fail',
                                      'subword': 'Second word is %2',
                                      'inside': ' (in the %NOUN)',
                                      },
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
        self.assertEqual(self.actions.message('subword'), ['Second word is numbered'])


    def test_pause(self):
        self.assertEqual(self.actions.pause(), 'PAUSE')


    def test_showdesc(self):
        self.assertEqual(self.actions.showdesc('start'), ['The starting room.'])
        self.assertEqual(self.actions.showdesc('window'), ['Made of glass.'])
        self.assertEqual(self.actions.showdesc('unicorn'), [])


    def test_shownotes(self):
        self.assertEqual(self.actions.shownotes('start|window'), ['Pass', 'Fail', 'Pass', 'Fail'])


    def test_showcontents_lists_names(self):
        self.assertItemsEqual(self.actions.showcontents('finish').split('\n'),
                              ('A window.', 'A bowl.'))


    def test_showcontents_lists_shortdescs(self):
        self.assertItemsEqual(self.actions.showcontents('finish', text='shortdesc').split('\n'),
                              ('You see a window.', 'A bowl is here.'))


    def test_showcontents_lists_recursively(self):
        self.assertItemsEqual(self.actions.showcontents('finish', recursive=True).split('\n'),
                              ('A window.', 'A bowl.', 'An apple.', 'A worm.'))


    def test_showcontents_lists_recursively_with_indent(self):
        self.assertItemsEqual(self.actions.showcontents('finish', recursive=True, indent=True)
                              .split('\n'),
                              ('A window.', 'A bowl.', '\tAn apple.', '\t\tA worm.'))


    def test_showcontents_lists_recursively_with_message(self):
        self.assertItemsEqual(self.actions.showcontents('finish', recursive=True, in_msg='inside')
                              .split('\n'),
                              ('A window.', 'A bowl.', 'An apple. (in the bowl)',
                               'A worm. (in the apple)'))


    def test_inv(self):
        pass
        # self.assertItemsEqual(self.actions.inv().split('\n'), ('Some money.',))


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
        self.actions.sendnoun('bowl', 'start')
        self.assertItemsEqual(self.state.noun_locs(self.bowl), [self.start])


    def test_sendtoroom(self):
        self.actions.sendtoroom('bowl')
        self.assertItemsEqual(self.state.noun_locs(self.bowl), [self.start])


    def test_sendtoinv(self):
        self.actions.sendtoinv('bowl')
        self.assertItemsEqual(self.state.noun_locs(self.bowl), ['INVENTORY'])


    def test_wear(self):
        self.actions.wear('bowl')
        self.assertItemsEqual(self.state.noun_locs(self.bowl), ['WORN'])


    def test_sendtonounloc(self):
        self.actions.sendtonounloc('unicorn', 'bowl')
        self.assertItemsEqual(self.state.noun_locs(self.unicorn), [self.finish])


    def test_sendtonounloc_works_for_dest_nouns_in_multiple_locations(self):
        self.actions.sendtonounloc('unicorn', 'window')
        self.assertItemsEqual(self.state.noun_locs(self.unicorn), [self.start, self.finish])


    def test_sendtonoun(self):
        self.actions.sendtonoun('unicorn', 'bowl')
        self.assertItemsEqual(self.state.noun_locs(self.unicorn), [self.bowl])


    def test_swapnouns(self):
        self.actions.swapnouns('bowl', 'window')
        self.assertItemsEqual(self.state.noun_locs(self.bowl), [self.start, self.finish])
        self.assertItemsEqual(self.state.noun_locs(self.window), [self.finish])


    def test_setnoundesc(self):
        self.actions.setnoundesc('bowl', 'pass')
        self.assertEqual(self.bowl.description, 'Pass')


    def test_addnounnote(self):
        self.actions.addnounnote('bowl', 'pass')
        self.assertEqual(self.bowl.notes, ['pass'])


    def test_addnounnote_with_multiple_notes(self):
        self.actions.addnounnote('bowl', 'pass', 'fail')
        self.assertEqual(self.bowl.notes, ['pass', 'fail'])


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
