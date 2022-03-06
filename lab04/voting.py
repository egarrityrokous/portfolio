# This module implements some useful functions, which will be eventually used
# to implement several different voting algorithms.

'''
This module implements some useful functions, which will be eventually used
to implement several different voting algorithms.
'''

__all__ = ['readBallot', 'firstChoice', 'uniques', 'mostVotes',
'leastVotes', 'majority', 'eliminateCandidate']

# Part 1, task 1
def readBallot(filename):
    #$ Good docstring
    ''' This function takes as input a file name, preferably a ballot list, and
    returns a list of lists of strings, with each inner list being a ballot of
    names (i.e. strings) a person voted for in an election.

    >>> readBallot('data/characters.csv')[6][2]
    'Elizabeth Bennet'
    >>> readBallot('data/example.csv')[7][0]
    'b'
    '''
    #$ Place comments above the line that you want to describe! This applies to all code you write.
    with open(filename) as ballotList:
        return [ballot.strip().split(',') for ballot in ballotList]
        # ballotList is separated, by line, into a new set of lists, each of
        # which are split into separate items by comma, and this new set of
        # lists is returned

# Part 1, task 2
def firstChoice(ballots):
    #$ Good, but could be clearer and more concise.
    ''' This function takes as input a list of a list of strings of candidates
    and outputs a list of the first items in the list originally inputted into
    the function. This function thus works extremely well in producing a list of
    voters' first choices in an election.

    >>> firstChoice(readBallot('data/simple.csv')[2:])
    ['Chris', 'Aamir']
    >>> firstChoice([['pie', 'tree'], ['hi', 'bye'], ['12', '123'], []])
    ['pie', 'hi', '12']
    '''

    return [ballot[0] for ballot in ballots if len(ballot) > 0]
    # for a list of ballots (each of which are a list themselves), only the
    # first candidate in each ballot is returned in a new list of first
    # candidate choices

# Part 1, task 3
def uniques(candidateList):
    ''' This function takes as input a list, preferably a ballot of names a
    person voted for in an election, and returns a new list of only the unique
    items in the originally inputted list.

    >>> uniques(['Bush', 'Gore', 'Nader', 'Gore', 'Bush'])
    ['Bush', 'Gore', 'Nader']
    >>> uniques(['12', '143', '134', '12', '123', '119', '134', '119'])
    ['12', '143', '134', '123', '119']
    '''

    uniqueNames = []
    for name in candidateList:
        if name not in uniqueNames:
            #$ uniqueNames.append(name) is more efficient then +=
            uniqueNames += [name]
    return uniqueNames
    # straight-forward way to return a new list of only unique items in a list

# Part 1, task 4
def mostVotes(firstChoiceList):
    ''' Takes as input a list of strings, preferably a list of first choice
    candidates in an election, and outputs a list of the most popular
    items in that originally inputted list.

    >>> mostVotes(['Clinton', 'Trump', 'Clinton', 'Johnson'])
    ['Clinton']
    >>> mostVotes(['pi', 'pi', 'hi', 'hi', 'bye', 'sigh', 'why', 'why', 'why'])
    ['why']
    '''

    mostPopular = []
    count = 0

    for mostVotedFor in firstChoiceList:
        if firstChoiceList.count(mostVotedFor) > count:
            count = firstChoiceList.count(mostVotedFor)
            mostPopular = [mostVotedFor]
        # if the number of times a candidate appears in firstChoiceList
        # is greater than the current count, count gets said number of times
        elif firstChoiceList.count(mostVotedFor) == count:
            mostPopular.append(mostVotedFor)
        # if number of times most popular candidate appears in firstChoiceList
        # is equal to count, candidate is added to accumulator list

    return uniques(mostPopular)
    # duplicates are removed from accumulator list

# Part 1, task 4
def leastVotes(firstChoiceList):
    ''' This function takes as input a list of strings, preferably a list
    of first choice candidates in an election, and returns a list of the least
    popular items in that originally inputted list.

    >>> leastVotes(['Obama','McCain','Obama','Obama','McCain','Nader','Barr'])
    ['Nader', 'Barr']
    >>> leastVotes(['pie', 'pie', 'why', 'why', 'why', 'hi', 'bye', 'sigh'])
    ['hi', 'bye', 'sigh']
    '''

    leastPopular = []
    count = len(firstChoiceList) #$ good choice for initialization!
    # the maximum length of firstChoiceList is the maximum number of votes
    # a candidate can get

    for leastVotedFor in firstChoiceList:
        if firstChoiceList.count(leastVotedFor) < count:
            count = firstChoiceList.count(leastVotedFor)
            leastPopular = [leastVotedFor]
            # if the number of times a candidate appears in firstChoiceList
            # is less than the current count, count gets said number of times,
            # and accumulator list is updated to that candidate
        elif firstChoiceList.count(leastVotedFor) == count:
            leastPopular.append(leastVotedFor)
        # when number of times least popular candidate appears in
        # firstChoiceList is equal to count, they're added to accumulator list

    return uniques(leastPopular)
    # duplicates are removed from accumulator list

# Part 1, task 5
def majority(firstChoiceList):
    ''' This function takes as input a list of strings, preferably a ballot
    list from an election, and returns True if an item on that list comes up
    more than 50% of the time time and returns False if that is not the case.

    >>> majority(['Biden', 'Trump', 'Jorgensen', 'Biden'])
    False
    >>> majority(['Bob', 'Bob', 'Vin', 'Bob', 'Bob', 'Vin', 'AJ', 'CJ', 'Bob'])
    True
    '''
    #$ What does this code do if given an empty list as input?
    n = len(firstChoiceList)
    # n is the maximum number of votes a candidate can possibly receive

    majorityVotedFor = mostVotes(firstChoiceList)[0]
    return firstChoiceList.count(majorityVotedFor) > n//2
    #$ Some of your comments could be more succinct
    # When there is a majority winner, majorityVotedFor will equal said person,
    # as that person received the most (and the majority of) first choice votes.
    # In the case of a tie, there will never be a majority winner anyway,
    # so this function will always return false when the if statement is run.

# Part 1, task 6
def eliminateCandidate(eliminationList, ballots):
    ''' This function takes as input a list of strings of candidates to
    eliminate and a list of ballots (a list of lists of strings), and it returns
    a new list of ballots (another list of lists of strings) that does not
    include the candidates to be eliminated but does include the rest of the
    candidates from the list of ballots.

    >>> eliminateCandidate(['Bob'], [['Bob', 'AJ', 'CJ'], ['Bob', 'CJ']])
    [['AJ', 'CJ'], ['CJ']]
    >>> eliminateCandidate(['a'], [['a', 'a', 'b'], ['a', 'b', 'c', 'c']])
    [['b'], ['b', 'c', 'c']]
    '''
    #$ Good work!
    candidateList = []

    for candidates in ballots:
        candidateList.append([person for person in candidates if person not in eliminationList])
    return candidateList
    # as ballots is a list of ballots (each of which are lists themselves),
    # for each ballot, each candidate is added to the new accumulator list so
    # long as they're not on eliminationList.
    # I am consciously letting line 169 go over 80 characters, by the way.

if __name__ == '__main__':
    # this allows us to run the doctests included in the functions above
    # when the file is run as a script
    from doctest import *
    testmod()
