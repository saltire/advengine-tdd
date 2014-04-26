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
            obj = args[0] # the tests or actions object

            # don't evaluate more selectors than there are arguments
            for i, stype in enumerate(self.stypes[:len(args) - 1]):
                arg = args[i + 1]
                if isinstance(arg, basestring):
                    # argument is a selector string: run selector method and filters
                    argparts = arg.split(':')
                    selector, filters = argparts[0], argparts[1:]

                    # get all items of this type, or selected items if a selector is passed
                    argitems = (getattr(self, 'all_' + stype)(obj) if selector in ('', '*')
                                else getattr(self, 'select_' + stype)(obj, selector))

                    # filter argitems to get only those items that pass each filter test given
                    # items will of course be filtered by the selector type of the filter method
                    for fstring in filters:
                        # skip filters that don't match 'filter_name' or 'filter_name(selector)'
                        m = re.match('^(\w*)(?:\(([\w%\|\*]*)\))?$', fstring)
                        try:
                            fname, fsel2 = m.group(1), m.group(2)
                        except AttributeError:
                            continue

                        fmethod = getattr(obj.tests, fname, None)
                        fargcount = len(getattr(fmethod, 'stypes', []))

                        if fargcount == 1:
                            # run one-argument filter on items
                            argitems = set(item for item in argitems if fmethod(set([item])))

                        elif fargcount == 2 and fsel2 is not None:
                            # run two-argument filter, using items and second argument
                            argitems = set(item for item in argitems
                                           if fmethod(set([item]), fsel2))

                    # replace selector argument with list of items
                    newargs[i + 1] = argitems

                else:
                    # argument is a set of items: filter by item type
                    newargs[i + 1] = arg & getattr(self, 'all_' + stype)(obj)

            return method(*newargs, **kwargs)

        # these are used when checking if we can use the method as a filter
        method_with_selection.stypes = self.stypes

        return method_with_selection


    def all_noun(self, obj):
        """Return all nouns."""
        return set(obj.state.nouns.itervalues())


    def all_room(self, obj):
        """Return all rooms."""
        return set(obj.state.rooms.itervalues())


    def all_entity(self, obj):
        """Return all nouns and rooms."""
        return self.all_noun(obj) | self.all_room(obj)


    def all_location(self, obj, items):
        """Return all locations."""
        return self.all_entity(obj) | set('INVENTORY', 'WORN')


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
