import re


def _filter_nouns(self, nfilter):
    """If passed a numerical wildcard, return nouns matching the
    corresponding input word. Otherwise, treat the filter as a pipe-
    delimited list of noun IDs and return those nouns."""
    if re.match('%(\d+)', nfilter) is not None:
        return self.state.nouns_by_input_word(int(nfilter[1:]))
    else:
        return set(self.state.nouns[nid] for nid in nfilter.split('|'))
    
    
def _filter_locations(self, lfilter):
    """If passed a numerical wildcard, return nouns matching the
    corresponding input word. Otherwise, treat the filter as a pipe-
    delimited list of location IDs and return those locations."""
    if re.match('%(\d+)', lfilter) is not None:
        return self.state.nouns_by_input_word(int(lfilter[1:]))
    else:
        return set(self.state.locations_by_id(lid)
                   for lid in lfilter.split('|'))
        
        
def noun_filter(test):
    """Replace the noun filter argument with a list of nouns."""
    def filtered_test(self, nfilter, *args):
        return test(self, _filter_nouns(self, nfilter), *args)
    return filtered_test
    
    
def location_filter(test):
    """Replace the location filter argument with a list of locations."""
    def filtered_test(self, lfilter, *args):
        return test(self, _filter_locations(self, lfilter), *args)
    return filtered_test
    
    
def noun_location_filter(test):
    """Replace the first filter argument with a list of nouns, and the second
    with a list of locations."""
    def filtered_test(self, nfilter, lfilter, *args):
        return test(self, _filter_nouns(self, nfilter),
                    _filter_locations(self, lfilter), *args)
    return filtered_test
    
