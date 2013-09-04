from collections import OrderedDict as odict
import json

from control import Control
from lexicon import Lexicon
from noun import Noun
from room import Room


class GameData:
    def __init__(self, data):
        # convert file to string
        try:
            data = data.read()
        except AttributeError:
            pass

        # convert string to dict
        try:
            data = self.import_from_json(data)
        except TypeError:
            pass

        # read data from dict
        self.nouns = {nid: Noun(ndata)
                      for nid, ndata in data.get('nouns', {}).items()}
        self.rooms = {rid: Room(rdata)
                      for rid, rdata in data.get('rooms', {}).items()}
        self.vars = {var: int(value)
                     for var, value in data.get('vars', {}).items()}
        self.messages = data.get('messages', {})
        self.lexicon = Lexicon(data.get('words', []))
        self.controls = {sid: ([Control(cdata) for cdata in stage]
                               if not isinstance(stage, (basestring, dict))
                               else [Control(stage)])
                         for sid, stage in data.get('controls', {}).items()}

        self.validate()


    def import_from_json(self, data):
        """Parse data string as JSON."""
        return json.loads(data, object_pairs_hook=odict)


    def validate(self):
        """Raise a ParseError if the game file contains any illegal data."""
        # room id conflicts with noun id
        for eid in set(self.rooms) & set(self.nouns):
            raise ParseError(1, eid)

        # room or noun id conflicts with reserved ids
        for eid in ('INVENTORY', 'WORN'):
            if eid in self.rooms or eid in self.nouns:
                raise ParseError(2, eid)



class ParseError(Exception):
    messages = {1: 'Room ID conflicts with noun ID: {0}',
                2: 'Room or noun ID conflicts with reserved ID: {0}'}

    def __init__(self, code, *args):
        self.code = code
        self.message = self.messages[code].format(*args)
