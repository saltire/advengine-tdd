class Control:
    def __init__(self, cdata):
        # check that control is a dict or an action string
        if isinstance(cdata, basestring):
            cdata = {'then': cdata}
        elif not isinstance(cdata, dict):
            raise TypeError

        # parse conditions (if...) into a list of lists of test strings
        conds = cdata.get('if', [])
        if isinstance(conds, basestring):
            # single test string - embed it in list of lists
            self.conds = [[conds]]
        elif len(conds) and all(isinstance(cond, basestring) for cond in conds):
            # list of test strings - embed it in list
            self.conds = [conds]
        else:
            # list of lists of test strings
            self.conds = conds

        # parse results (then/else...) into a list of controls or actions
        def parse_results(results):
            if isinstance(results, (basestring, dict)):
                # single action string or control - embed it in list
                results = [results]

            # add each result as a new control or an action
            return [Control(result) if isinstance(result, dict) else result
                    for result in results]

        self.true_results = parse_results(cdata.get('then', []))
        self.false_results = parse_results(cdata.get('else', []))


    def get_actions(self, tests):
        """Run each set of tests for this control, and if all tests are true
        for any set of tests, return the 'then' actions, otherwise 'else'."""
        def test_is_true(test):
            method, args = test.split()[0], test.split()[1:]
            return getattr(tests, method)(*args)

        results = (self.true_results if not self.conds
                   or any(all(test_is_true(test) for test in cond)
                                       for cond in self.conds)
                   else self.false_results)

        actions = []

        for result in results:
            if isinstance(result, Control):
                # run tests for this control and return its actions
                actions.extend(result.get_actions(tests))
            else:
                # return the actions
                action, args = result.split()[0], result.split()[1:]
                actions.append((action, args))

        return actions
