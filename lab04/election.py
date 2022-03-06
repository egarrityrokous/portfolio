# Implements different voting rules

'''
This module implements different voting rules using functions in another
module, voting.py, to show how voting rules matter.
'''

# import functions from voting module
from voting import *

#$ See comments in voting.py about commenting style.
def plurality(ballots):
    '''Takes as input ballot data as a list of lists of strings, and
    returns a list of strings of names of candidates who get the most votes.

    >>> plurality(readBallot('data/simple.csv'))
    ['Aamir']
    >>> plurality(readBallot('data/example.csv'))
    ['a']
    >>> plurality(readBallot('data/characters.csv'))
    ['Scarlett O’Hara', 'Samwise Gamgee']
    '''
    return mostVotes(firstChoice(ballots))
    # straight-forward way to determine the plurality winner of an election

def borda(ballots):
    '''Takes as input ballot data as list of lists of strings, and
    returns a list of strings of the names of candidates with the
    maximum borda score.

    >>> borda(readBallot('data/simple.csv'))
    ['Aamir']
    >>> borda(readBallot('data/example.csv'))
    ['c']
    >>> borda(readBallot('data/characters.csv'))
    ['Harry Potter']
    '''

    n = len(ballots[0]) # n = the total number of candidates
    bordaList = []
    for ballot in ballots:
        for candidate in ballot:
            bordaList.extend([candidate] * n) #$ good
            n -= 1
            # loop adds candidate to bordaList n times, where n represents
            # number of first place votes, n-1 represents number of second place
            # votes, etc.
        n = len(ballots[0])
        # reset n so algorithm can correctly iterate over each ballot in ballots
    return mostVotes(bordaList)
    # the candidate with the greatest borda score will now appear the most times
    # in bordaList

def rankedChoice(ballots):
    '''Takes as input ballot data as list of lists of strings, and
    returns the winner of the election based on ranked-choice
    voting as a list of strings of names.

    >>> rankedChoice(readBallot('data/simple.csv'))
    ['Aamir']
    >>> rankedChoice(readBallot('data/example.csv'))
    ['b']
    >>> rankedChoice(readBallot('data/characters.csv'))
    ['Scarlett O’Hara']
    '''
    #$ What happens if given empty lists as input? eg, rankedChoice ([[], []])
    while not majority(firstChoice(ballots)):
        ballots = eliminateCandidate(leastVotes(firstChoice(ballots)), ballots)
    return mostVotes(firstChoice(ballots))
    # while there is not a majority winner in ballots, we eliminate the
    # candidate with the least amount of first choice votes. Then we return
    # the candidate who finally has a majority of first votes left in ballots,
    # who is the eventual winner of any ranked choice election tested with this
    # ballot reading algorithm.

def condorcet(ballots):
    '''EXTRA CREDIT: Takes as input ballot data as list of
    lists of strings, and returns the winner of the Condorcet election
    as a string (or empty string if there is no Condorcet winner).
    '''
    pass

if __name__ == '__main__':
    from doctest import *
    testmod()
    classBallots = readBallot('data/icecream.csv')
    print('Ice-cream flavor class election results:')
    print('Plurality winner:', *plurality(classBallots))
    print('Borda winner:', *borda(classBallots))
    print('Ranked-choice winner:', *rankedChoice(classBallots))

    # eliminate the winning flavor and try again
    winningFlavor = plurality(classBallots)[0]
    newBallots = eliminateCandidate([winningFlavor], classBallots)
    print('\nUpdated icecream flavor election results:')
    print('Plurality winner:', *plurality(newBallots))
    print('Borda winner:', *borda(newBallots))
    print('Ranked-choice winner:', *rankedChoice(newBallots))

    ## Uncomment the following line if you complete the extra credit
    #print('Condorcet winner:', condorcet(classBallots))
