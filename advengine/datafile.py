from collections import OrderedDict as odict
import json


class DataFile:
    def __init__(self, path):
        with open(path) as dfile:
            data = dfile.read()
        
        fn = 'import_from_{0}'.format(path.rsplit('.', 1)[1])
        self.data = getattr(self, fn)(data)
    
    
    def import_from_json(self, data):
        return json.loads(data, object_pairs_hook=odict)
        
        
    