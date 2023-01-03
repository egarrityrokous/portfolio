from collections import defaultdict


class Factor:
    """A factor in a Bayesian network (i.e. a multivariable function)"""

    def __init__(self, variables, values):
        """
        Parameters
        ----------
        variables : list[str]
            The variables of the factor
        values : dict[tuple[str], float]
            A dictionary mapping each event (expressed as a tuple) to its value
        """

        self._variables = variables
        self._values = values
    
    def get_variables(self):
        """Returns the variables of the factor.

        Returns
        -------
        list[Variable]
            The variables of the factor.
        """

        return self._variables

    def get_value(self, event):
        """Returns the value that the factor assigns to a particular event.

        Returns
        -------
        float
            The value associated with the event

        Raises
        ------
        KeyError
            If the factor has no value assigned to the given event.
        """

        key = []
        for var in self._variables:
            if var not in event:
                raise KeyError(f'Variable {var} not found in given event.')
            key.append(event[var])
        if tuple(key) in self._values:
            return self._values[tuple(key)]
        else:
            raise KeyError(f'No value assigned to event {event}.')

    def normalize(self):
        """Normalizes the event values.

        In other words, each event value is divided by the overall sum of the event
        values so that they all sum to one.

        Returns
        -------
        Factor
            A new Factor, identical to the current Factor, except that the event values
            are normalized.
        """
        new_values = dict()
        event_vals_total = sum([v for v in self._values.values()])
        for event, value in self._values.items():
            if event_vals_total == 0:
                new_values[event] = 0
            else:
                new_values[event] = value / event_vals_total

        return Factor(self._variables, new_values)

    def reduce(self, evidence):
        """Removes any events in the factor that do not agree with the "evidence" event.

        An event "does not agree" with another event if the two events associate different
        domain values with some variable. For instance, the following events agree:
            {'P': 'yes', 'D': 's', 'R': '+'}
            {'P': 'yes', 'D': 's', 'T': '-'}
        because there is no variable associated with different values in the two events.
        However:
            {'P': 'yes', 'D': 'n', 'R': '+'}
            {'P': 'yes', 'D': 's', 'T': '-'}
        do not agree, since the variable 'D' is associated with different values in the
        events.

        Parameters
        ----------
        evidence : dict[str, str]
            The "evidence" event.

        Returns
        -------
        Factor
            A new Factor, identical to the current Factor, except that events that disagree
            with the evidence event are removed.
        """
        new_values = self._values.copy()
        for event in self._values:
            for idx, variable in enumerate(self._variables):
                if variable not in evidence:
                    # e.g. first example shown above, where 'R' is not in evidence
                    continue
                evidence_value = evidence[variable]
                event_value = event[idx]
                if evidence_value != event_value:
                    # disagreement found
                    del new_values[event]
                    break
        
        return Factor(self._variables, new_values)

    def marginalize(self, variable):
        """Marginalizes (sums) out the specified variable.

        Parameters
        ----------
        variable : Variable
            The variable to marginalize out.

        Returns
        -------
        Factor
            A new Factor, identical to the current Factor with the specified variable
            marginalized out.
        """
        new_values = dict()
        idx = self._variables.index(variable)
        for event, value in self._values.items():
            # remove `variable` from event
            new_event = list(event)
            new_event.pop(idx)
            new_event = tuple(new_event)
            # update value for the event that doesn't include this variable
            new_values[new_event] = new_values.get(new_event, 0) + value

        vars_to_keep = self._variables.copy()
        vars_to_keep.pop(idx)
        return Factor(vars_to_keep, new_values)

    def __str__(self):
        result = f"{self._variables}:"
        for event, value in self._values.items():
            result += f"\n  {event}: {value}"
        return result

    __repr__ = __str__


def events(vars, domains):
    """
    Takes a list of variables and returns the cross-product of the domains.

    For instance, suppose the domain of variable X is ('a', 'b') and the
    domain of the variable Y is ('c','d','e'). Then:

       >>> X = Variable('X', ('a', 'b'))
       >>> Y = Variable('Y', ('c', 'd', 'e'))
       >>> events([X, Y])
       [('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'c'), ('b', 'd'), ('b', 'e')]
    """
    first_var = vars.pop()
    first_var_domain = domains[first_var]
    res = [{first_var: first_var_domain[i]} for i in range(len(first_var_domain))]

    # while we still have unprocessed vars
    while vars:

        new_res = []
        next_var = vars.pop()
        next_var_domain = domains[next_var]

        # while there are still events in res that we haven't processed 
        # to add outcomes for next_var
        while res:
            event = res.pop()
            # add all possible outcomes for this var to each existing event
            for outcome in next_var_domain:
                extended_event = event.copy()
                extended_event[next_var] = outcome
                new_res.append(extended_event)

        res = new_res

    return res

def multiply_factors(factors, domains):
    """Multiplies a list of factors.

    Parameters
    ----------
    factors : list[Factor]
        The factors to multiply
    domains : dict[str, list[str]]
        A dictionary mapping each variable to its possible values

    Returns
    -------
    Factor
        The product of the input factors.
    """
    unioned_variables = set()
    for factor in factors:
        unioned_variables = unioned_variables.union(set(factor.get_variables()))
    unioned_variables = list(unioned_variables)
    variables_indices = {var: idx for (idx, var) in enumerate(unioned_variables)}

    all_events = events(unioned_variables.copy(), domains)
    new_values = dict()
    for event in all_events:
        # event is a dict mapping variable: outcome
        # order the outcomes according to the order of variables in unioned_variables
        key = [(variable, outcome) for variable, outcome in event.items()]
        key.sort(key = lambda x:variables_indices[x[0]])
        key = tuple([x[1] for x in key])

        # compute the value for this event
        value = 1
        for factor in factors:
            # which variables does this factor give us information about?
            query = {var: outcome for (var, outcome) in event.items() if var in factor.get_variables()}

            try:
                factor_value = factor.get_value(query)
                value *= factor_value
                vars_to_consider = vars_to_consider - set(factor.get_variables())
            except:
                continue

        new_values[key] = value

    return Factor(unioned_variables, new_values)



