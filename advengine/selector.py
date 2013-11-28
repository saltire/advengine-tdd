import re


class selector:
    """A decorator class that can be applied to tests and actions, to automatically
    convert selector strings into corresponding sets of objects."""

    def __init__(self, *stypes):
        """Store the types of selectors that will be expected as arguments."""
        self.stypes = stypes


    def __call__(self, method):
        """For each selector type specified, treat the next argument passed
        to the method as a selector of that type, replace it with the
        selected set of objects, and call the method with the new arguments."""
        def method_with_selection(*args, **kwargs):
            newargs = list(args)
            obj = args[0]

            # don't evaluate more selectors than there are arguments
            for i, stype in enumerate(self.stypes[:len(args) - 1]):
                arg = args[i + 1]
                if isinstance(arg, basestring):
                    # argument is a selector string: run selector method and filters
                    argparts = arg.split(':')
                    selector, filters = argparts[0], argparts[1:]
                    # call selector function and get set of items
                    argitems = getattr(self, 'select_' + stype)(obj, selector)
                    # filter argitems to get only those items that pass each filter test given
                    for fname in filters:
                        fmethod = getattr(obj.tests, fname)
                        argitems = set(item for item in argitems if fmethod(set([item])))
                    # replace selector argument with list of items
                    newargs[i + 1] = argitems

                else:
                    # argument is a set of items: filter by item type
                    newargs[i + 1] = getattr(self, 'filter_' + stype)(obj, arg)


            return method(*newargs, **kwargs)

        return method_with_selection


    def filter_noun(self, obj, items):
        """Given a set of items, return the nouns."""
        return set(item for item in items if item in obj.state.nouns.itervalues())


    def filter_room(self, obj, items):
        """Given a set of items, return the rooms."""
        return set(item for item in items if item in obj.state.rooms.itervalues())


    def filter_entity(self, obj, items):
        """Given a set of items, return the nouns and rooms."""
        return set(item for item in items if (item in obj.state.nouns.itervalues()
                                              or item in obj.state.rooms.itervalues()))


    def filter_location(self, obj, items):
        """Given a set of items, return the locations."""
        return set(item for item in items if (item in obj.state.nouns.itervalues()
                                              or item in obj.state.rooms.itervalues()
                                              or item in ('INVENTORY', 'WORN')))


    def select_noun(self, obj, selector):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the selector as a pipe-
        delimited list of noun IDs and return those nouns."""
        if re.match('%(\d+)', selector) is not None:
            return obj.state.nouns_by_input_word(int(selector[1:]))
        else:
            return set(obj.state.nouns[nid] for nid in selector.split('|')
                       if nid in obj.state.nouns)


    def select_room(self, obj, selector):
        """Treat the selector as a pipe-delimited list of room IDs
        and return those rooms."""
        return set(obj.state.rooms[rid] for rid in selector.split('|')
                   if rid in obj.state.rooms)


    def select_location(self, obj, selector):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the selector as a pipe-
        delimited list of location IDs and return those locations."""
        if re.match('%(\d+)', selector) is not None:
            return obj.state.nouns_by_input_word(int(selector[1:]))
        else:
            return set(obj.state.locations_by_id(lid) for lid in selector.split('|')
                       if obj.state.locations_by_id(lid))


    def select_entity(self, obj, selector):
        """If passed a numerical wildcard, return nouns matching the
        corresponding input word. Otherwise, treat the selector as a pipe-
        delimited list of noun or room IDs and return those nouns/rooms."""
        if re.match('%(\d+)', selector) is not None:
            return obj.state.nouns_by_input_word(int(selector[1:]))
        else:
            return set(obj.state.nouns.get(oid) or obj.state.rooms.get(oid)
                       for oid in selector.split('|')
                       if (oid in obj.state.nouns or oid in obj.state.rooms))
