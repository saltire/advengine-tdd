import unittest

from advengine.noun import Noun


class Test_Noun(unittest.TestCase):
    def setUp(self):
        self.noun = Noun({'desc': "Description",
                          'notes': ['pass']
                          })
        
        
    def test_description_setter(self):
        self.noun.set_description("New description")
        self.assertEqual(self.noun.description, "New description")
        
        
    def test_add_note_appends_notes_to_end_of_list(self):
        self.noun.add_note('fail', 'fail')
        self.assertEqual(self.noun.notes, ['pass', 'fail', 'fail'])


    def test_remove_note_removes_all_instances_of_note(self):
        self.noun.notes = ['one', 'two', 'three', 'two']
        self.noun.remove_note('one', 'two')
        self.assertEqual(self.noun.notes, ['three'])
        
        
    def test_clear_note_removes_all_notes(self):
        self.noun.clear_notes()
        self.assertEqual(self.noun.notes, [])
        
        