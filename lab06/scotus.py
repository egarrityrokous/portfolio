# Support function for analyzing the decisions of the Supreme Court.
# Much of this work follows that of Fowler (see paper directory).

"""
This module provides a number of methods that support the analysis of
Supreme Court of the United States (SCOTUS) decisions.

It provides three important functions:
   readDecisions - read yearly dockets of cases and their citation counts
   hIndex - given a list of citation counts, compute the 'h-index'
   plotImpacts - plot the h-index for each year's docket of cases
"""
import csv
import matplotlib.pyplot as plt

__all__ = ['readDecisions', 'hIndex', 'plotImpacts']

def readDecisions(filename):
    """
    This function takes the name of a CSV file (string) containing Supreme Court
    data and creates a dictionary that maps a year (int) to that year's docket
    (a tuple of case citation counts).

    >>> len(readDecisions('data/judicial.csv'))
    235
    >>> db = readDecisions('data/judicial.csv')
    >>> (min(db), max(db))  # range of dates for decisions
    (1754, 2002)
    >>> max(readDecisions('data/judicial.csv'))
    2002
    >>> readDecisions('data/judicial.csv')[1793]
    (0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 31, 0, 0, 0, 0, 0)
    >>> [ year in db for year in [ 1753, 1754, 1755 ] ]
    [False, True, False]
    >>> db[1783]
    (0, 1, 0)
    >>> db[1784]
    (1, 0, 1, 0, 0, 0, 0, 0, 1, 0)
    >>> 1754 in db
    True
    >>> len(db[2002])
    17
    """
    # a dictionary that maps a year (key) to a tuple of citation counts (indeg)
    db = dict()

    with open(filename) as caseFile:
        for row in csv.reader(caseFile):
            # ignores the top header line in caseFile
            #$ Good check!
            if row[0].isdigit():

            # extracts relevant info in each row (year, indeg)
                year = int(row[3])
                indeg = int(row[8])

            # updates dictionary (db)
                db[year] = db.get(year,()) + (indeg,)

    # return the accumulated data
    return db

def hIndex(counts):
    """Computes and returns the h-index (int) of counts (tuple of citation counts).
    A citation list has an h-index of i if:
       1) the i largest values in the list are i or greater, and
       2) i is the maximum such value.

    >>> hIndex( (0, 2, 15, 9, 7, 48, 4, 82, 14, 6) )
    6
    >>> hIndex( (4, 4, 4, 4, 4) )
    4
    >>> hIndex( () )
    0
    >>> hIndex( (20, 11, 7, 3, 3, 1, 1, 0, 0) )
    3
    """
    # sorts counts by descending value
    hIndexTuple = sorted(counts, reverse = True)

    hIndexValue = 0 # starts with hIndex value of 0

    #$ Well-written!
    for count in hIndexTuple:
        if count > hIndexValue:
            hIndexValue += 1
    return hIndexValue

def plotImpacts(db, plotFilename):
    """Generate a line plot of the h-index associated with each year in
    the database, db (dictionary).  Plot saved as file with name found in
    plotFilename (string).
    """
    # extracts all the years in db into a list, sorted into increasing order.
    yearsList = sorted(db.keys())

    dictValues = db.values()
    hIndexList = []
    for tuple in dictValues:
        # appends h-index for each year's case citations to hIndexListFinal
        hIndexList.append(hIndex(tuple))

    # generates line plot of h-index values for each year's case citations and
    # saves plot using plot filename provided
    plt.title('H-Index by Year of Supreme Court Decisions')
    plt.xlabel('Year')
    plt.ylabel('H-Index')
    plt.plot(yearsList, hIndexList, 'b-')
    plt.savefig(plotFilename)

def test():
    """Exercise document tests."""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

    # 1. read in decisions
    db = readDecisions('data/judicial.csv')

    # 2. plot their impacts
    plotImpacts(db, 'scotusImpact.pdf')
