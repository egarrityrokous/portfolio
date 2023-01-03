import numpy as np
import os
from factor import Factor, events
from bayes import BayesianNetwork


class FamilyMember:
    """A single member of a family tree."""

    def __init__(self, name, sex, mother, father):
        """
        Parameters
        ----------
        name : str
            The name of the family member.
        sex : str
            The sex of the family member ("male" or "female")
        mother : FamilyMember
            The mother of the family member (or None if unknown)
        father : FamilyMember
            The father of the family member (or None if unknown)
        """

        self.name = name
        self.sex = sex
        self.mother = mother
        self.father = father

    def get_name(self):
        """Returns the name of the family member."""
        return self.name

    def get_sex(self):
        """Returns the sex of the family member."""
        return self.sex


class Male(FamilyMember):
    """A male family member."""

    def __init__(self, name, mother=None, father=None):
        super().__init__(name, "male", mother, father)


class Female(FamilyMember):
    """A female family member."""

    def __init__(self, name, mother=None, father=None):
        super().__init__(name, "female", mother, father)


def romanoffs():
    """A simple example of a family, using four members of the Russian royal family (the Romanoffs)."""
    alexandra = Female("alexandra")
    nicholas = Male("nicholas")
    alexey = Male("alexey", mother=alexandra, father=nicholas)
    anastasia = Female("anastasia", mother=alexandra, father=nicholas)
    return alexandra, nicholas, alexey, anastasia


def create_variable_domains(family):
    """Creates a dictionary mapping each variable to its domain, for the hemophilia network.

    For each family member, we create either 3 or 4 variables (3 if they’re male, 4 if they’re female).
    If N is the name of the family member, then we create the following variables:
        M_N: N’s maternally inherited gene
        P_N: N’s paternally inherited gene (if N is female)
        G_N: the genotype of N
        H_N: whether N has hemophilia

    The variables should be mapped to the following domains:
        - M_N: ['x', 'X']
        - P_N: ['x', 'X']
        - G_N: ['xx', 'xX', 'XX']
        - H_N: ['-', '+']

    Parameters
    ----------
    family : list[FamilyMember]
        the list of family members

    Returns
    -------
    dict[str, list[str]]
        a dictionary mapping each variable to its domain (i.e. its possible values)
    """
    male_variable_templates = {"M_": ['x', 'X'], "G_": ['xy', 'Xy'], "H_": ['-', '+']}

    female_variable_templates = male_variable_templates.copy()
    female_variable_templates['P_'] = ['x', 'X']
    female_variable_templates['G_'] = ['xx', 'xX', 'XX']

    res = dict()
    for member in family:
        if member.get_sex() == 'male':
            for (variable, domain) in male_variable_templates.items():
                res[variable + member.get_name()] = domain
        else:
            for (variable, domain) in female_variable_templates.items():
                res[variable + member.get_name()] = domain

    return res  


def create_hemophilia_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of hemophilia, given one's genotype.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of hemophilia, given one's genotype
    """
    variables = ["G_" + person.get_name(), "H_" + person.get_name()]
    domains = create_variable_domains([person])

    all_events = events(variables.copy(), domains)
    values = dict()
    for event in all_events:
        # (value for H_, value for G_)
        # P(-, xy) = 1
    
        h_val = event["H_" + person.get_name()]
        g_val = event["G_" + person.get_name()]
    
        if h_val == "+":
            if person.get_sex() == "male" and g_val == "Xy":
                values[(g_val, h_val)] = 1
            elif person.get_sex() == "female" and event["G_" + person.get_name()] == "XX":
                values[(g_val, h_val)] = 1
            else:
                values[(g_val, h_val)] = 0
        else:
            if person.get_sex() == "male" and event["G_" + person.get_name()] != "Xy":
                values[(g_val, h_val)] = 1
            elif person.get_sex() == "female" and event["G_" + person.get_name()] != "XX":
                values[(g_val, h_val)] = 1
            else:
                values[(g_val, h_val)] = 0
    
    return Factor(variables, values)


def create_genotype_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of a genotype, given one's inherited genes.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of a genotype, given one's inherited genes
    """
    domains = create_variable_domains([person])

    if person.get_sex() == "male":
        variables = ["G_" + person.get_name(), "M_" + person.get_name()]
        all_events = events(variables.copy(), domains)

        values = dict()
        for event in all_events:
            g_val = event["G_" + person.get_name()]
            m_val = event["M_" + person.get_name()]
        
            if m_val == "X":
                if g_val == "Xy":
                    values[(g_val, m_val)] = 1
                else:
                    values[(g_val, m_val)] = 0

            else:
                if g_val == "xy":
                    values[(g_val, m_val)] = 1
                else:
                    values[(g_val, m_val)] = 0

    else:
        variables = ["G_" + person.get_name(), "M_" + person.get_name(), "P_" + person.get_name()]
        all_events = events(variables.copy(), domains)

        values = {
            ("XX", "X", "X"): 1,
            ("xX", "X", "X"): 0,
            ("xx", "X", "X"): 0,

            ("XX", "x", "X"): 0,
            ("xX", "x", "X"): 1,
            ("xx", "x", "X"): 0,
            
            ("XX", "X", "x"): 0,
            ("xX", "X", "x"): 1,
            ("xx", "X", "x"): 0,
            
            ("XX", "x", "x"): 0,
            ("xX", "x", "x"): 0,
            ("xx", "x", "x"): 1,
            
            ("XX", "X", "x"): 0,
            ("xX", "x", "x"): 0
        }

    return Factor(variables, values)


def create_maternal_inheritance_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of the gene inherited from one's mother.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of the gene inherited from the family member's mother.
    """
    if not person.mother:
        values = {
            ('x',): 29999/30000,
            ("X",): 1/30000
        }
        return Factor(["M_" + person.get_name()], values)
    
    mother = person.mother
    variables = ["M_" + person.get_name(), "G_" + mother.get_name()]
    values = {
        ('X', 'XX'): 1,
        ('X', 'xX'): 0.5,
        ('X', 'xx'): 0,
        ('x', 'XX'): 0,
        ('x', 'xX'): 0.5,
        ('x', 'xx'): 1
    }

    return Factor(variables, values)


def create_paternal_inheritance_cpt(person):
    """Creates a conditional probability table (CPT) specifying the probability of the gene inherited from one's father.

    Parameters
    ----------
    person : FamilyMember
        the family member whom the CPT pertains to

    Returns
    -------
    Factor
        a Factor specifying the probability of the gene inherited from the family member's father.
    """
    if not person.father:
        values = {
            ('x',): 29999/30000,
            ("X",): 1/30000
        }
        return Factor(["P_" + person.get_name()], values)
    
    father = person.father
    variables = ["P_" + person.get_name(), "G_" + father.get_name()]
    values = {
        ('X', 'Xy'): 1,
        ('X', 'xy'): 0,
        ('x', 'Xy'): 0,
        ('x', 'xy'): 1
    }

    return Factor(variables, values)


def create_family_bayes_net(family):
    """Creates a Bayesian network that models the genetic inheritance of hemophilia within a family.

    Parameters
    ----------
    family : list[FamilyMember]
        the members of the family

    Returns
    -------
    BayesianNetwork
        a Bayesian network that models the genetic inheritance of hemophilia within the specified family
    """
    domains = create_variable_domains(family)
    cpts = []
    for person in family:
        if person.get_sex() == "female":
            cpts.append(create_paternal_inheritance_cpt(person))
        cpts.append(create_maternal_inheritance_cpt(person))
        cpts.append(create_genotype_cpt(person))
        cpts.append(create_hemophilia_cpt(person))
    return BayesianNetwork(cpts, domains)


