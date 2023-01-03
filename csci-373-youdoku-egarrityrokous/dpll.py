import cnf
from cnf import Clause, Literal, Cnf
from util import SearchSpace, dfs
from random import shuffle
from search import SatisfiabilitySearchSpace
from collections import defaultdict

def unit_resolve(unit_clauses, clause):
    """Resolves a clause with a set of unit clauses.

    This function resolves the provided clause simultaneously with all
    of the provided unit clauses as follows:
    - If the clause contains the same literal as one of the unit clauses,
      e.g. the clause is !A || !B || C and one the unit clauses is !B, then
      the clause is redundant (entailed by that unit clause) and therefore
      unnecessary. Hence None should be returned.
    - Otherwise, any clause literals whose negations appear in a unit clause
      should be removed, e.g. if the clause is !A || !B || C || !D and the unit
      clauses contain both A and !C, then the resolved clause should be !B || D.

    Parameters
    ----------
    unit_clauses : set[Clause]
        The set of unit clauses.
    clause : Clause
        The clause to resolve with the unit clauses.

    See the examples in test.TestUnitResolve to gain further insight into
    the expected behavior of this function.

    Returns
    -------
    Clause
        The resolved clause (or None if the original clause is redundant)
    """
    result = []
    target_literals = clause.get_literals()
    for literal in target_literals:
        neg_unit_clause = Clause([literal.negate()])
        if Clause([literal]) in unit_clauses and len(clause) > 1: #if the literal already exists
            return None
        if neg_unit_clause not in unit_clauses: #if the negation of the literal exists
            result.append(literal)
    return Clause(result)

def unit_resolution(unit_clauses, regular_clauses):
    """Resolves a set of clauses with a set of unit clauses.

    This function resolves each regular clause AND unit clause with each unit clause,
    using the unit_resolve function.

    Attention: resolution can produce new unit clauses, and these unit clauses
    must also be resolved with all the other clauses. The process should continue
    until no new clauses can be created through unit resolution.

    See the examples in test.TestUnitResolution to gain further insight into
    the expected behavior of this function.

    Parameters
    ----------
    unit_clauses : set[Clause]
        The set of unit clauses.
    regular_clauses : set[Clause]
        The set of non-unit clauses.

    Returns
    -------
    set[Clause], set[Clause]
        The resolved unit clauses and non-unit clauses, respectively.
    """
    unit_clauses = set(unit_clauses)
    regular_clauses = set(regular_clauses)
    while True:
        newClauses = set()
        new_unit_clauses = set()
        allClauses = regular_clauses | unit_clauses
        for c1 in allClauses:
            newClause = unit_resolve(unit_clauses, c1)
            if newClause is None: #it already exists in the state
                continue
            if len(newClause) == 1: #it is a new unit clause
                new_unit_clauses.add(newClause)
            else:  # or it is a new clause
                newClauses.add(newClause)
        #the prev reg clauses are not meaningful next iteration because
        #their resolutions were just calculated, so we only leave new clauses
        regular_clauses = newClauses
        #if they are even no changes/ resolutions were made
        if len(unit_clauses) == len(new_unit_clauses):
            break
        unit_clauses = new_unit_clauses
        #if len(regular_clauses) == 0: #if there are possible unit resolutions, unsatisfiable
            #regular_clauses.add(cnf.c('FALSE'))
    return unit_clauses, regular_clauses
class DpllSearchSpace(SatisfiabilitySearchSpace):
    """A search space for the DPLL algorithm."""

    def __init__(self, sent):
        """
        Parameters
        ----------
        sent : Cnf
            a CNF sentence for which we want to find a satisfying model

        """

        super().__init__(sent)
        unit_clauses = set()
        regular_clauses = set()
        for clause in sent.clauses:
            if len(clause) == 1:
                unit_clauses.add(clause)
            else:
                regular_clauses.add(clause)
        self.unit_clauses, self.regular_clauses = unit_resolution(unit_clauses, regular_clauses)

    def get_successors(self, state):
        """Computes the successors of a DPLL search state.

        A search state is a tuple of literals, one for each symbol in the signature.
        As with the SatisfiabilitySearchSpace, the successors of state
        (l_1, ..., l_k) should typically be (l_1, ..., l_k, !s_{k+1}) and
        (l_1, ..., l_k, s_{k+1}), where s_{k+1} is the (k+1)th symbol in the
        signature (according to an alphabetical ordering of the signature symbols).

        However:
        - if self.sent conjoined with literals l_1, ..., l_k entails False (according
          to unit resolution), then there should be no successors, i.e. this method
          should return an empty list
        - if self.sent conjoined with literals l_1, ..., l_k entails !s_{k+1}
          (according to unit resolution), then the only successor should be
          (l_1, ..., l_k, !s_{k+1})
        - if self.sent conjoined with literals l_1, ..., l_k entails s_{k+1},
          (according to unit resolution), then the only successor should be
          (l_1, ..., l_k, s_{k+1}).

        See the examples in test.TestDpllSearchSpace to gain further insight into
        the expected behavior of this method.

        Tips:
        - You can get the "False" clause using the expression cnf.c("FALSE")
        - When you generate both successors (i.e. for both !s_{k+1} and s_{k+1}),
          put the !s_{k+1} successor first in the returned list.

        Parameters
        ----------
        state : tuple[Literal]
            The literals currently assigned by the search node

        Returns
        -------
        list[tuple[Literal]]
            The successor states.
        """
        stateClauses = set([Clause([literal]) for literal in state])
        unit_clauses = self.unit_clauses | stateClauses #all unit clauses
        #update unit and regular clause variables for this next state
        unit_clauses, regular_clauses = unit_resolution(unit_clauses, self.regular_clauses)
        if (cnf.c("FALSE")) in regular_clauses:
            return []
        #next_literal = Literal(self.signature[len(state)])
        #if next_literal.negate() in unit_clauses:
            #print("hello2")
            #return tuple(list(state) + [next_literal.negate()])
        #if next_literal in unit_clauses:
            #print("ho ho2")
            #return tuple(list(state) + [next_literal])
        result = []
        successor = self.signature[len(state)]
        next_literal = None
        for clause in unit_clauses:
            if successor == clause.get_literals()[0].get_symbol():
                next_literal = clause.get_literals()[0]
        if next_literal is not None:
            result.append(state + tuple([next_literal]))
        else:
            for value in [False, True]:
                next_literal = Literal(successor, value)
                result.append(state + tuple([next_literal]))
        return result

def dpll(sent):
    """An implementation of the DPLL algorithm for satisfiability.

    This function will only work once DpllSearchSpace is correctly implemented.

    Parameters
    ----------
    sent : cnf.Sentence
        the CNF sentence for which we want to find a satisfying model.

    Returns
    -------
    dict[str, bool]
        a satisfying model (if one exists), otherwise None is returned
    """

    search_space = DpllSearchSpace(sent)
    state, _ = dfs(search_space)
    model = {lit.get_symbol(): lit.get_polarity() for lit in state} if state is not None else None
    return model
