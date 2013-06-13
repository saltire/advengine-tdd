import unittest

from advengine.room import Room


class Test_Room(unittest.TestCase):
    
    def setUp(self):
        self.room = Room({'desc': 'Description',
                          'notes': ['pass']
                          })


    def test_description_setter(self):
        self.room.set_description("New description")
        self.assertEqual(self.room.description, "New description")
        
        
    def test_add_note_appends_notes_to_end_of_list(self):
        self.room.add_note('fail', 'fail')
        self.assertEqual(self.room.notes, ['pass', 'fail', 'fail'])


    def test_remove_note_removes_all_instances_of_note(self):
        self.room.notes = ['one', 'two', 'three', 'two']
        self.room.remove_note('one', 'two')
        self.assertEqual(self.room.notes, ['three'])
        
        
    def test_clear_note_removes_all_notes(self):
        self.room.clear_notes()
        self.assertEqual(self.room.notes, [])
        
