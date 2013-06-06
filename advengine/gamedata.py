from collections import OrderedDict as odict
import json

from control import Control
from lexicon import Lexicon
from noun import Noun
from room import Room


class GameData:
    def __init__(self, data):
        # if string is passed, treat it as a file path and read that file
        if isinstance(data, basestring):
            with open(data) as dfile:
                rawdata = dfile.read()
            
            fn = 'import_from_{0}'.format(data.rsplit('.', 1)[1])
            data = getattr(self, fn)(rawdata)
    
        self.nouns = {nid: Noun(ndata) for nid, ndata in data.get('nouns', {}).items()}
        self.rooms = {rid: Room(rdata) for rid, rdata in data.get('rooms', {}).items()}
        self.vars = data.get('vars', {})
        self.messages = data.get('messages', {})
        self.lexicon = Lexicon(data.get('words', []))
        self.controls = {sid: [Control(cdata) for cdata in stage]
                         for sid, stage in data.get('controls', {}).items()}
        
        
    def import_from_json(self, data):
        """Parse data string as JSON."""
        return json.loads(data, object_pairs_hook=odict)
        
        
    