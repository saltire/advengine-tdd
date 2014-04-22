from collections import OrderedDict as odict
import json

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
        self.nouns = odict((nid, Noun(ndata)) for nid, ndata in data.get('nouns', {}).iteritems())
        self.rooms = odict((rid, Room(rdata)) for rid, rdata in data.get('rooms', {}).iteritems())
        self.vars = odict((var, int(value)) for var, value in data.get('vars', {}).iteritems())
        self.messages = data.get('messages', {})
        self.lexicon = Lexicon(data.get('words', []))
        self.controls = odict((stage, ([self.parse_control(cdata) for cdata in scontrols]
                                       if not isinstance(scontrols, (basestring, dict))
                                       else [self.parse_control(scontrols)]))
                              for stage, scontrols in data.get('controls', {}).iteritems())

        self.validate()


    def import_from_json(self, data):
        """Parse data string as JSON."""
        return json.loads(data, object_pairs_hook=odict)


    def validate(self):
        """Raise a ParseError if the game file contains any illegal data."""
        # room id conflicts with noun id
        for eid in set(self.rooms) & set(self.nouns):
            raise GameDataError(1, eid)

        # room or noun id conflicts with reserved ids
        for eid in ('INVENTORY', 'WORN'):
            if eid in self.rooms or eid in self.nouns:
                raise GameDataError(2, eid)

        # no starting room
        start = [rid for rid, room in self.rooms.iteritems() if room.is_start]
        if len(start) < 1:
            raise GameDataError(3)
        elif len(start) > 1:
            raise GameDataError(4, ', '.join(start))


    def parse_control(self, cdata):
        # check that control is a dict or an action string
        if isinstance(cdata, basestring):
            cdata = {'then': cdata}
        elif not isinstance(cdata, dict):
            raise TypeError

        # parse conditions (if...) into a list of lists of test strings
        conds = cdata.get('if', [])
        if isinstance(conds, basestring):
            # single test string - embed it in list of lists
            conds = [[conds]]
        elif len(conds) and all(isinstance(cond, basestring) for cond in conds):
            # list of test strings - embed it in list
            conds = [conds]
        else:
            # list of lists of test strings
            conds = conds

        # parse results (then/else...) into a list of controls or actions
        def parse_results(results):
            if isinstance(results, (basestring, dict)):
                # single action string or control - embed it in list
                results = [results]

            # add each result as a new control or an action
            return [self.parse_control(result) if isinstance(result, dict) else result
                    for result in results]

        return {'if': conds,
                'then': parse_results(cdata.get('then', [])),
                'else': parse_results(cdata.get('else', [])),
                }


class GameDataError(Exception):
    messages = {1: 'Room ID conflicts with noun ID: {0}',
                2: 'Room or noun ID conflicts with reserved ID: {0}',
                3: 'No starting room specified.',
                4: 'Multiple starting rooms specified: {0}'}

    def __init__(self, code, *args):
        self.code = code
        self.message = self.messages[code].format(*args)
