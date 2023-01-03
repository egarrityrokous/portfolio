from collections import defaultdict
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree


def run_inference(bnet, evidence):
    """Computes all single variable distributions, conditioned on the evidence.
    This should return a dictionary that maps each variable v to P(v | evidence).
    These distributions should be computed using the junction tree algorithm
    discussed in class.
    Parameters
    ----------
    bnet : BayesianNetwork
        the Bayesian network
    evidence : dict[str, str]
        the evidence event (represented as a dictionary mapping variables to values)
    Returns
    -------
    dict[str, Factor]
        a dictionary that maps each variable v to P(v | evidence)
    """

    return belief_propagation(bnet, evidence)


def message_passing(jtree, compute_leaf_msg, compute_msg):
    """Runs a general message-passing algorithm over a junction tree.
    Parameters
    ----------
    jtree : JunctionTree
        the junction tree
    compute_leaf_msg : lambda leaf: ...
        a one-argument function that computes the message that a leaf node (represented
        as its integer index in the junction tree) sends to its only neighbor
    compute_msg : lambda src, dest, msgs: ...
        a three-argument function that computes the message that node src (represented
        as its integer index in the junction tree) sends to node dest; the third
        argument msgs is a set containing the messages sent from src's other neighbors
        (not including dest) to src.
    Returns
    -------
    dict[(int, int), object]
        a dictionary mapping each edge to its message
    """

    def update_ready_list(node):
        if len(waiting_for[node]) == 1:
            neighbor = list(waiting_for[node])[0]
            if (node, neighbor) not in messages:
                ready_to_process.add((node, neighbor))
        elif len(waiting_for[node]) == 0:
            for neighbor in jtree.get_neighbors(node):
                if (node, neighbor) not in messages:
                    ready_to_process.add((node, neighbor))
    messages = dict()
    leaves = [node for node in range(jtree.get_num_nodes()) if jtree.is_leaf(node)]
    for leaf in leaves:
        only_neighbor = jtree.get_neighbors(leaf)[0]
        messages[(leaf, only_neighbor)] = compute_leaf_msg(leaf)
    waiting_for = [set() for _ in range(jtree.get_num_nodes())]
    for (node1, node2) in jtree.get_edges():
        if (node2, node1) not in messages:
            waiting_for[node1].add(node2)
        if (node1, node2) not in messages:
            waiting_for[node2].add(node1)
    ready_to_process = set()
    for node in range(len(waiting_for)):
        update_ready_list(node)
    while len(ready_to_process) > 0:
        src, dest = ready_to_process.pop()
        other_neighbors = set(jtree.get_neighbors(src)) - {dest}
        msgs = [messages[(neighbor, src)] for neighbor in other_neighbors]
        messages[(src, dest)] = compute_msg(src, dest, msgs)
        waiting_for[dest].remove(src)
        update_ready_list(dest)
    return messages

def count_nodes(jtree):
    """Computes the number of nodes in a junction tree.
    This is just an example showing how the general message passing algorithm
    can be used.
    Parameters
    ----------
    jtree : JunctionTree
        the junction tree
    Returns
    -------
    int
        the number of nodes in the junction tree
    """

    messages = message_passing(jtree,
                               lambda leaf: 1,
                               lambda src, dest, msgs: 1 + sum(msgs))
    for (src, dest) in messages:
        if jtree.is_leaf(dest):
            return 1 + messages[(src, dest)]


def compute_separators(jtree):
    """Computes the separator of each edge of a junction tree.
    The separator is the set of variables that appear in factors on both sides
    of the edge. In other words, if we removed the edge from the tree, creating
    two separate trees, separator variables are the ones that appear in the
    factors of both trees.
    Parameters
    ----------
    jtree : JunctionTree
        the junction tree
    Returns
    -------
    dict[(int, int), set[int]]
        a dictionary that ssociates each junction tree edge with its separators
    """

    separators = dict()
    messages = message_passing(jtree,
                               lambda leaf: set(jtree.get_factor(leaf).get_variables()),
                               lambda src, dest, msgs: set.union(*msgs))
    for (node1, node2) in jtree.get_edges():
        separators[(node1, node2)] = messages[(node1, node2)] & messages[(node2, node1)]
        separators[(node2, node1)] = messages[(node1, node2)] & messages[(node2, node1)]
    return separators


def belief_propagation(bnet, evidence):
    """Computes all single variable distributions, conditioned on the evidence.
    This should return a dictionary that maps each variable v to P(v | evidence).
    These distributions should be computed using the junction tree algorithm
    discussed in class.
    Parameters
    ----------
    bnet : BayesianNetwork
        the Bayesian network
    evidence : dict[str, str]
        the evidence event (represented as a dictionary mapping variables to values)
    Returns
    -------
    dict[str, Factor]
        a dictionary that maps each variable v to P(v | evidence)
    """

    def compute_msg(src, dest, msgs):
        message = multiply_factors(msgs, bnet.get_domains())
        for v in message.get_variables():
            if v not in separators[(src, dest)]:
                message = message.marginalize(v)
        return message
    jtree = build_junction_tree(bnet)
    separators = compute_separators(jtree)
    messages = message_passing(jtree,
                               lambda leaf: jtree.get_factor(leaf).reduce(evidence),
                               compute_msg)
    single_var_marginals = dict()
    for src, dest in messages:
        if jtree.is_leaf(dest):
            factors = [messages[(src, dest)], jtree.get_factor(dest).reduce(evidence)]
            marginal = multiply_factors(factors, bnet.get_domains())
            for variable in marginal.get_variables():
                if variable not in single_var_marginals:
                    new_marginal = marginal
                    for other in marginal.get_variables():
                        if other != variable:
                            new_marginal = new_marginal.marginalize(other)
                    single_var_marginals[variable] = new_marginal.normalize()
    return single_var_marginals


class JunctionTree:
    """A junction tree."""

    def __init__(self, graph, factors):
        """
        Parameters
        ----------
        graph : UndirectedGraph
            the tree structure of the junction tree
        factors : dict[int, list[Factor]]
            a dictionary mapping leaf nodes to their factors
        """

        self._graph = graph
        self._factors = factors
        self._separators = None

    def get_num_nodes(self):
        """Returns the number of nodes in the junction tree.
        Returns
        -------
        int
            the number of nodes in the junction tree
        """

        return self._graph.get_num_nodes()

    def get_edges(self):
        """Returns the edges in the junction tree.
        Returns
        -------
        list[(int, int)]
            a list of the edges in the junction tree
        """

        return self._graph.get_edges()

    def get_neighbors(self, node):
        """Returns the neighbors of a particular node in the junction tree.
        Parameters
        ----------
        node : int
            the node of interest
        Returns
        -------
        list[int]
            a list of neighbors, i.e. nodes that have an edge connecting them to the node of interest
        """

        return self._graph.get_neighbors(node)

    def get_factor(self, node):
        """Returns the factor associated with a particular node of the junction tree.
        If the node doesn't have an associated factor, then this method returns None.
        Parameters
        ----------
        node : int
            the node of interest
        Returns
        -------
        Factor
             the factor associated with the specified node, or None if there isn't one
        """

        if node < len(self._factors) and len(self._factors[node]) == 1:
            return self._factors[node][0]
        else:
            return None

    def is_leaf(self, node):
        """Returns whether a node is a leaf node.
        Parameters
        ----------
        node : int
            the node of interest
        Returns
        -------
        bool
             True if the node is a leaf, i.e. has exactly one neighbor
        """

        return self._graph.is_leaf(node)

    def __str__(self):
        result = ""
        for node in range(self._graph.get_num_nodes()):
            if self.is_leaf(node):
                result += f'\nnode {node} {self._factors[node]}'
            else:
                result += f'\nnode {node} (neighbors: {self.get_neighbors(node)})'
        return result


class BayesianNetwork:
    """Represents a Bayesian network by its factors, i.e. the conditional probability tables (CPTs).
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

        relevant = []
        irrelevant = []
        for factor in self.get_factors():
            if variable in factor.get_variables():
                relevant.append(factor)
            else:
                irrelevant.append(factor)
        new_factor = multiply_factors(relevant, self.get_domains())
        new_factor = new_factor.marginalize(variable)
        return BayesianNetwork(irrelevant + [new_factor], self.get_domains())

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
        """Computes the conditional distibution over a set of variables given evidence.
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


class Factor:

    def __init__(self, variables, values):
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

        normalizer = sum([v for _, v in self._values.items()])
        return Factor(self._variables, {k: v / normalizer for (k, v) in self._values.items()})

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

        reduced_values = dict()
        for event in self._values:
            keep_row = True
            for var, value in zip(self._variables, event):
                if var in evidence and evidence[var] != value:
                    keep_row = False
            if keep_row:
                reduced_values[event] = self._values[event]
        return Factor(self._variables, reduced_values)

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

        if variable not in self._variables:
            raise Exception('Variable {} not found.'.format(variable))
        else:
            variable_index = self._variables.index(variable)
            other_variables = self._variables[0:variable_index] + self._variables[variable_index + 1:]
            new_values = defaultdict(float)
            for event in self._values:
                marginalized = tuple([v for (k, v) in zip(self._variables, event) if k != variable])
                new_values[marginalized] += self._values[event]
            return Factor(other_variables, dict(new_values))

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

    def convert_event_to_dict(event):
        result = dict()
        for (var, value) in zip(vars, event):
            result[var] = value
        return result

    def events_helper(variables):
        if len(variables) == 0:
            return [()]
        if len(variables) == 1:
            return [[val] for val in domains[variables[0]]]
        else:
            first_var = variables[0]
            other_events = events_helper(variables[1:])
            result = []
            for value in domains[first_var]:
                for event in other_events:
                    result.append([value] + event)
            return result

    return [convert_event_to_dict(event) for event in events_helper(vars)]


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

    def event_to_tuple(variables):
        return tuple([event[var] for var in variables])

    all_vars = set()
    for factor in factors:
        all_vars = all_vars | set(factor.get_variables())
    all_vars = list(all_vars)
    values = dict()
    for event in events(all_vars, domains):
        try:
            product = 1.0
            for factor in factors:
                product *= factor.get_value(event)
            values[event_to_tuple(all_vars)] = product
        except KeyError:
            pass
    return Factor(all_vars, values)

def compute_elimination_order(bnet):
    """Computes a low-width elimination order for a Bayesian network.
    YOU DO NOT NEED TO UNDERSTAND HOW THIS FUNCTION WORKS.
    Parameters
    ----------
    bnet : BayesianNetwork
        the Bayesian network for which to compute the elimination order
    Returns
    -------
    list[str]
        the elimination order (a list of the variables of the Bayesian network)
    """

    def build_moral_graph(bnet):
        node_labels = [var for var in bnet.get_variables()]
        edges = []
        for factor in bnet.get_factors():
            vars = [v for v in factor.get_variables()]
            for i, var in enumerate(vars):
                edges += [(var, neighbor) for neighbor in vars[:i] + vars[i + 1:]]
        return UndirectedGraph(len(node_labels), edges, node_labels)

    def min_degree_elim_order(moral_graph):
        def min_degree_node(adjacency):
            best, best_degree = None, float("inf")
            for node in adjacency:
                if len(adjacency[node]) < best_degree:
                    best, best_degree = node, len(adjacency[node])
            return best

        adjacencies = moral_graph.get_adjacencies()
        elim_order = []
        while len(adjacencies) > 0:
            min_degree = min_degree_node(adjacencies)
            adjacencies = {n: adjacencies[n] - {min_degree} for n in adjacencies if n != min_degree}
            elim_order.append(min_degree)
        return elim_order
    moral_graph = build_moral_graph(bnet)
    return min_degree_elim_order(moral_graph), moral_graph


def build_junction_tree(bnet):
    """Constructs a junction tree from a Bayesian network.
    YOU DO NOT NEED TO UNDERSTAND HOW THIS FUNCTION WORKS.
    Parameters
    ----------
    bnet : BayesianNetwork
        the Bayesian network
    Returns
    -------
    JunctionTree
        a reasonably efficient junction tree for the provided Bayesian network
    """

    def elimination_cliques():
        result = []
        adjacencies = moral_graph.get_adjacencies()
        for node in elim_order:
            result.append(adjacencies[node] | {node})
            neighbors = adjacencies[node]
            new_adjacencies = dict()
            for n in adjacencies:
                if n in neighbors:
                    new_adjacencies[n] = (adjacencies[n] - {node}) | (neighbors - {n})
                elif n != node:
                    new_adjacencies[n] = adjacencies[n]
            adjacencies = new_adjacencies
        return result

    elim_order, moral_graph = compute_elimination_order(bnet)
    cliques = elimination_cliques()
    adjacency_matrix = np.zeros((len(cliques), len(cliques)), int)
    for i in range(len(cliques)):
        for j in range(i + 1, len(cliques)):
            adjacency_matrix[i][j] = -len(cliques[i] & cliques[j])
    mst = minimum_spanning_tree(adjacency_matrix)
    edges = zip(mst.nonzero()[0], mst.nonzero()[1])
    graph = UndirectedGraph(num_nodes=len(elim_order), node_labels=list(range(len(elim_order))), edges=edges)
    builder = JunctionTreeBuilder(graph, cliques)
    for factor in bnet.get_factors():
        builder.add_factor(factor)
    junction_tree = builder.get_junction_tree()
    return prune_unlabeled_leaves(junction_tree)


class UndirectedGraph:
    """A undirected graph."""

    def __init__(self, num_nodes, edges, node_labels=None):
        self.num_nodes = num_nodes
        if node_labels is None:
            node_labels = [None for _ in range(num_nodes)]
        self.node_labels = node_labels
        self.adjacency = defaultdict(set)
        for (node1, node2) in edges:
            self.adjacency[node1].add(node2)
            self.adjacency[node2].add(node1)
        self.adjacency = dict(self.adjacency)

    def get_neighbors(self, node):
        return list(self.adjacency[node])

    def is_leaf(self, node):
        return len(self.get_neighbors(node)) == 1

    def are_adjacent(self, node1, node2):
        return node2 in self.adjacency[node1]

    def get_adjacencies(self):
        return self.adjacency

    def get_num_nodes(self):
        return self.num_nodes

    def get_node_label(self, index):
        return self.node_labels[index]

    def prune_leaf(self, index):
        assert self.is_leaf(index)
        new_edges = []
        for (x, y) in self.get_edges():
            if x != index and y != index:
                new_edge = [x, y]
                if x > index:
                    new_edge[0] -= 1
                if y > index:
                    new_edge[1] -= 1
                new_edges.append(tuple(new_edge))
        return UndirectedGraph(self.num_nodes-1, new_edges, self.node_labels[:index] + self.node_labels[index+1:])

    def get_edges(self):
        result = set()
        for node in self.adjacency:
            for neighbor in self.adjacency[node]:
                edge = tuple(sorted([node, neighbor]))
                result.add(edge)
        return sorted(result)

    def sprout_leaf(self, node, node_label=None):
        new_node = self.num_nodes
        new_edge = (new_node, node)
        return new_node, UndirectedGraph(self.num_nodes+1,
                                         self.get_edges() + [new_edge],
                                         self.node_labels + [node_label])


    def __str__(self):
        return str(self.get_edges())


def prune_unlabeled_leaves(jtree):
    def first_unlabeled_leaf():
        for node in range(result._graph.get_num_nodes()):
            if result._graph.is_leaf(node) and len(result._factors[node]) == 0:
                return node
        else:
            return None
    result = jtree
    prunable_leaf = first_unlabeled_leaf()
    while prunable_leaf is not None:
        new_graph = result._graph.prune_leaf(prunable_leaf)
        new_factors = result._factors[:prunable_leaf] + result._factors[prunable_leaf+1:]
        result = JunctionTree(new_graph, new_factors)
        prunable_leaf = first_unlabeled_leaf()
    return result


class JunctionTreeBuilder:

    def __init__(self, graph, clusters):
        self.graph = graph
        self.clusters = clusters
        self.node_map = defaultdict(set)
        for node, cluster in enumerate(self.clusters):
            for variable in cluster:
                self.node_map[variable].add(node)
        self.node_map = dict(self.node_map)
        self.factors = defaultdict(list)

    def add_factor(self, factor):
        nodesets = [self.node_map[var] for var in factor.get_variables()]
        possible_assignments = nodesets[0]
        for nodeset in nodesets[1:]:
            possible_assignments = possible_assignments & nodeset
        assignment = list(possible_assignments)[0]
        if not self.graph.is_leaf(assignment):
            assignment, self.graph = self.graph.sprout_leaf(assignment)
        elif len(self.factors[assignment]) > 0:
            assignment1, self.graph = self.graph.sprout_leaf(assignment)
            self.factors[assignment1] = self.factors[assignment]
            self.factors[assignment] = []
            assignment, self.graph = self.graph.sprout_leaf(assignment)
        self.factors[assignment].append(factor)

    def get_junction_tree(self):
        factor_list = [[] for _ in range(self.graph.get_num_nodes())]
        for i, factor in self.factors.items():
            factor_list[i] = factor
        return JunctionTree(self.graph, factor_list)