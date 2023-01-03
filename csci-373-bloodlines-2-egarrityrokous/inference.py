from collections import defaultdict
from util import compute_elimination_order, build_junction_tree
from factor import multiply_factors
from bayes import BayesianNetwork

# Change this flag to True once you've implemented belief propagation.
ACTIVATE_BELIEF_PROPAGATION = True

def run_inference(bnet, evidence):
    if ACTIVATE_BELIEF_PROPAGATION:
        return belief_propagation(bnet, evidence)
    else:
        cond_dist = bnet.compute_conditional(["G_elizabeth_ii"], evidence)
        return {'G_elizabeth_ii': cond_dist}

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
        a dictionary that associates each junction tree edge with its separators
    """

    def unpack_msgs(src, dest, msgs):
        s = set()
        for msg in msgs:
            for v in msg:
                s.add(v)
        return tuple(s)

    messages = message_passing(jtree,
                               lambda leaf: tuple(jtree.get_factor(leaf).get_variables()),
                               unpack_msgs)

    res = dict()
    for (src, dest) in messages:
        incoming = set(messages[(src, dest)])
        outgoing = set(messages[(dest, src)])
        separators = incoming.intersection(outgoing)
        res[(src, dest)] = separators
        res[(dest, src)] = separators
    
    return res


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

    # update bnet given the evidence we observed
    new_factors = list()
    for factor in bnet.get_factors():
        for var in factor.get_variables():
            if var in evidence:
                factor = factor.reduce(evidence)
        new_factors.append(factor)

    domains = bnet.get_domains()
    for (var, outcome) in evidence.items():
        # remove outcomes that aren't possible given the observed evidence
        domains[var] = [outcome]

    # now, running the jtree algo with give conditional probabilities instead of marginal
    new_bnet = BayesianNetwork(new_factors, domains)

    jtree = build_junction_tree(new_bnet)
    separators = compute_separators(jtree)

    """"
    From lecture slides:
    (1) leaf nodes send their factor to their only neighbor, after marginalizing out
        non-separator vars
    (2) each internal node waits to recieve factors from its neighbors. Once it's
        received all factors but one, it can send a factor to its remaining neighbor.
        This new factor will be the product of the received factors... after
        marginalizing out variables not in the separator with that neighbor.
    Note: wording of (2) is kind of confusing. We need to compute the product, THEN
    marginalize out the non-separator variables.
    """

    # implement (1) as described above
    def compute_leaf_msg(leaf):
        leaf_separators = None
        for (src, dest) in separators:
            if src == leaf:
                leaf_separators = separators[(src, dest)]
        
        leaf_factor = jtree.get_factor(leaf)
        leaf_vars = leaf_factor.get_variables()
        non_separators = set(leaf_vars) - leaf_separators

        for var in non_separators:
            leaf_factor = leaf_factor.marginalize(var)
    
        return leaf_factor
    
    # implement (2) as described above
    def compute_msg(src, dest, msgs):
        # msgs contains the factors that have been received
        # First, compute product of the factors
        all_domains = bnet.get_domains()
        all_variables = [var for factor in msgs for var in factor.get_variables()]
        domains = {variable: outcomes for variable, outcomes in all_domains.items() if variable in all_variables}
        factor_product = multiply_factors(msgs, domains)
        
        # Next, marginalize out the non-separator vars
        node_separators = separators[(src, dest)]
        non_separators = set(factor_product.get_variables()) - node_separators
        for var in non_separators:
            factor_product = factor_product.marginalize(var)
            
        return factor_product
        

    messages = message_passing(jtree,
                               compute_leaf_msg,
                               compute_msg)

    """"
    From lecture slides:
    To compute a single-variable marginal:
        1. choose a leaf containing the variable
        2. multiply its factor with its received "message"
        3. marginalize out other variables 
    """

    result = dict()
    for (src, dest) in messages:
        if jtree.is_leaf(dest):
            leaf_factor = jtree.get_factor(dest)
            leaf_vars = leaf_factor.get_variables()

            # if we've already computed the single var marginals for all vars in this node, continue
            vars_to_compute = []
            for var in leaf_vars:
                if var not in result:
                    vars_to_compute.append(var)
    
            if len(vars_to_compute) == 0:
                continue
    
            received_factor = messages[(src, dest)]
            received_vars = received_factor.get_variables()
        
            domains = dict()
            bnet_domains = bnet.get_domains()
            for var in leaf_vars + received_vars:
                if var not in domains:
                    domains[var] = bnet_domains[var]

            factor_product = multiply_factors([leaf_factor, received_factor], domains)

            for var in vars_to_compute:
                res_factor = factor_product

                # marginalize out all other vars
                for v in factor_product.get_variables():
                    if v != var:
                        res_factor = res_factor.marginalize(v)

                result[var] = res_factor.normalize()

    return result

