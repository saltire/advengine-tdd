import re


class selector:
    def __init__(self, *stypes):
        self.stypes = stypes


    def __call__(self, method):
        """For each selection type specified, treat the next argument passed
        to the method as a selector of that type, replace it with the
        selected set of objects, and call the method with the new arguments."""
        def method_with_selection(*args, **kwargs):
            newargs = list(args)
            for i, stype in enumerate(self.stypes):
                newargs[i + 1] = getattr(self, 'select_' + stype)(args[0],
                                                                  args[i + 1])
            return method(*newargs, **kwargs)
        return method_with_selection


    def select_noun(self, obj, selector):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the selector as a pipe-
        delimited list of noun IDs and return those nouns."""
        if re.match('%(\d+)', selector) is not None:
            return obj.state.nouns_by_input_word(int(selector[1:]))
        else:
            return set(obj.state.nouns[nid] for nid in selector.split('|'))


    def select_room(self, obj, selector):
        """Treat the selector as a pipe-delimited list of room IDs
        and return those rooms."""
        return set(obj.state.rooms[rid] for rid in selector.split('|'))


    def select_location(self, obj, selector):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the selector as a pipe-
        delimited list of location IDs and return those locations."""
        if re.match('%(\d+)', selector) is not None:
            return obj.state.nouns_by_input_word(int(selector[1:]))
        else:
            return set(obj.state.locations_by_id(lid)
                       for lid in selector.split('|'))


    def select_entity(self, obj, selector):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the selector as a pipe-
        delimited list of noun or room IDs and return those nouns/rooms."""
        if re.match('%(\d+)', selector) is not None:
            return obj.state.nouns_by_input_word(int(selector[1:]))
        else:
            return set(obj.state.nouns.get(oid) or obj.state.rooms.get(oid)
                       for oid in selector.split('|'))
