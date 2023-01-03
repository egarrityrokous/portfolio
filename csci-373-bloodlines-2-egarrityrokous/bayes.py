from util import UndirectedGraph
from factor import multiply_factors
from util import compute_elimination_order


class BayesianNetwork:
    """Represents a Bayesian network by its factors (i.e. the CPTs).

    Parameters
    ----------
    factors : list[factor.Factor]
        The factors of the Bayesian network
    domains : dict[str, list[str]]
        A dictionary mapping each variable to its possible values
    """

    def __init__(self, factors, domains):
        self._factors = factors
        self._domains = domains
        self._variables = set()
        for factor in self._factors:
            self._variables = self._variables | set(factor.get_variables())

    def get_variables(self):
        """Returns the set of variables that appear in at least one factor."""
        return self._variables

    def get_domains(self):
        """Returns the variable signature associated with the Bayesian network."""
        return self._domains

    def get_factors(self):
        """Returns the factors of the Bayesian network."""
        return self._factors

    def eliminate(self, variable):
        """Eliminates a variable from the Bayesian network.

        By "eliminate", we mean that the factors containing the variable are multiplied,
        and then the variable is marginalized (summed) out of the resulting factor.

        Parameters
        ----------
        variable : str
            the variable to eliminate from the Bayesian network

        Returns
        -------
        BayesianNetwork
            a new BayesianNetwork, equivalent to the current Bayesian network, after
            eliminating the specified variable
        """
        new_domains = {k: v for (k, v) in self._domains.items() if k != variable}

        new_factors = []
        factors_with_eliminated_var = []
        for factor in self.get_factors():
            if variable in factor.get_variables():
                factors_with_eliminated_var.append(factor)
            else:
                new_factors.append(factor)
    
        variables = set()
        for factor in factors_with_eliminated_var:
            variables = variables.union(set(factor.get_variables()))
        
        domains = {v: outcomes for (v, outcomes) in self._domains.items() if v in variables}

        product_factor = multiply_factors(factors_with_eliminated_var, domains)
        result_factor = product_factor.marginalize(variable)

        new_factors.append(result_factor)

        return BayesianNetwork(new_factors, new_domains)

    def compute_marginal(self, vars):
        """Computes the marginal probability over the specified variables.

        This method uses variable elimination to compute the marginal distribution.

        Parameters
        ----------
        vars : set[str]
            the variables that we want to compute the marginal over
        """

        elim_order, _ = compute_elimination_order(self)
        bnet = self
        revised_elim_order = [var for var in elim_order if var not in vars]
        for var in revised_elim_order:
            bnet = bnet.eliminate(var)
        return multiply_factors(bnet.get_factors(), bnet.get_domains())

    def compute_conditional(self, vars, evidence):
        """Computes the conditional distibution over a set of variables given an evidence event.

        Parameters
        ----------
        vars : list[str]
            the variables that we want to compute the probability distribution over
        evidence : dict[str, str]
            the observed event

        Returns
        -------
        float
            the conditional probability of the event according to the Bayesian network
        """

        all_vars = list(vars) + list(evidence.keys())
        marginal = self.compute_marginal(all_vars)
        marginal = marginal.reduce(evidence)
        for var in evidence:
            marginal = marginal.marginalize(var)
        return marginal.normalize()

    def __str__(self):
        return '\n\n'.join([str(factor) for factor in self._factors])
