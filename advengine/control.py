class Control:
    def __init__(self, cdata):
        
        if isinstance(cdata, basestring):
            cdata = {'then': cdata}
            
        conds = cdata.get('if', [])
        if isinstance(conds, str):
            self.conds = [[conds]]
        elif conds and isinstance(conds[0], basestring):
            self.conds = [conds]
        else:
            self.conds = conds
             
        def parse_actions(results):
            if not isinstance(results, list):
                results = [results]
                
            return [Control(result) if isinstance(result, dict) else result
                    for result in results]
            
        parse_results = lambda a: [a] if isinstance(a, basestring) else a
        self.true_results = parse_results(cdata.get('then', []))
        self.false_results = parse_results(cdata.get('else', []))
        
        
    def get_actions(self, tests):
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
                actions.extend(result.get_actions(tests))
            else:
                action, args = result.split()[0], result.split()[1:]
                actions.append((action, args))

        return actions
        