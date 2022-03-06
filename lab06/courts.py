# Evaluate the impact of each Chief Justice's court.
# Extended work for the SCOTUS lab.
"""
This module supports the analysis of the supreme court cases heard
during each Chief Justice's term.
   readCourts - given a citation database, assemble docket for each CJ
   rankCourts - a database of court dockets, develop a ranked list of impacts
"""
import csv
from scotus import *
__all__ = ['readCourts', 'rankCourts']

def readCourts(justiceFilename,dockets):
    """Given a justiceFilename (string) a path to csv file of Chief Justices and
    their terms (name, start-year, end-year) and a database of case citation
    counts, dockets (dict), assemble and return a dictionary that maps the name
    of a justice to a tuple of case citations.

    >>> len(readCourts('data/chiefJustices.csv', readDecisions('data/judicial.csv')))
    16
    >>> db = readDecisions('data/judicial.csv')
    >>> cjdb = readCourts('data/chiefJustices.csv', db)
    >>> cjdb['John Rutledge'] == db[1795]
    True
    """
    #$ Good job working through the logic of this question!
    cjd = dict() # dictionary accumulator
    justiceTuple = () # tuple accumulator for each Chief Justice
    with open(justiceFilename) as f:
        for row in csv.reader(f):
            # makes sure we're only looking at rows for each Chief Justice
            if row[2].isdigit():
                justice = row[0] # justice gets justice name
                termStart = int(row[1])
                termEnd = int(row[2])
                for year in dockets:
                    # if year in dockets is an element of [termStart,termEnd]
                    # the value of that year, a tuple, is concatenated to
                    # tuple accumulator
                    if year in range(termStart,termEnd+1):
                        justiceTuple += dockets[year]
                # dictionary accumulator gets Chief Justice names as keys and
                # accumulator tuple as value
                cjd[justice] = cjd.get(justice,()) + justiceTuple
                # accumulator tuple is reset before we iterate over next justice
                justiceTuple = ()
    return cjd

def byImpact(pair):
    """A 'key function' for used in sorted.

    >>> byImpact( ('John Jay', 5 ) )
    5
    """
    _, impact = pair
    return impact

def rankCourts(cjdb):
    """Construct a list of (justice, hIndex) pairs sorted in decreasing order
    of hIndex given cjdb (dict).

    >>> db = readDecisions('data/judicial.csv')
    >>> cjdb = readCourts('data/chiefJustices.csv', db)
    >>> rankCourts(cjdb)[-2]
    ('John Jay', 5)
    >>> db = readDecisions('data/judicial.csv')
    >>> courtDB = readCourts('data/chiefJustices.csv',db)
    >>> jjCourt = courtDB['John Jay']
    >>> len(jjCourt)
    146
    >>> max(jjCourt)
    31
    >>> jjCourt.index(31)
    104
    >>> hIndex(jjCourt)
    5
    """
    pairListInitial = [] # initial accumulator list
    index = 0
    justiceKeys = list(cjdb.keys()) # list of keys in given dictionary
    justiceTuples = list(cjdb.values()) # list of values in given dictionary
    for justice in justiceKeys:
        # concatenates (justice, hIndex) pairs to initial accumulator list
        pairListInitial += [(justice, hIndex(justiceTuples[index]))]
        index += 1
    # sorts (justice, hIndex) pairs in decreasing order by hIndex value
    pairListFinal = sorted(pairListInitial, key = byImpact, reverse = True)
    return pairListFinal

def test():
    """Exercise document tests."""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

    # 1. Read in the scotus database
    db = readDecisions('data/judicial.csv')

    # 2. Read in the court impacts
    courtDB = readCourts('data/chiefJustices.csv',db)

    # 3. Build rankings
    ranking = rankCourts(courtDB)

    # 4. Print the rankings out
    for court, impact in ranking:
        print("{}: {}".format(court,impact))
