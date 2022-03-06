# This module contains puzzle problems from NPR and the Spelling Bee from The New York Times

from wordTools import * # imports functions from wordTools.py

def b1(): # for Part 2 of Lab03
    """Returns an int representing the number of lowercase 7-letter isograms
    that are the answer to the puzzle B1"""
    count = 0
    for word in readWords('words/dict.txt'):
        if word.islower() and isIsogram(word) and 7 == len(word): # if word is isogram and 7 letters long, add it to accumulator
            count += 1
    return count

def p1(): # for secondary extra credit (for fun?)
    """Return a string representing the concatenation of the two body parts
    that are the answers to puzzle P1"""
    for part1 in readWords('words/bodyParts.txt'):
        if len(part1) == 6:
            part1 = part1 + 'r' # add 'r' to every body part with 6 letters
            for part2 in readWords('words/bodyParts.txt'):
                if canon(part1) == canon(part2): # if the letters of part1 + 'r' equal the letters of part2
                    #$ Is there another way to achieve this goal without slicing?
                    part1 = part1[0:6] # taking out the previously 'r'
                    return part1 + ' ' + part2


def p2(): # for Part 2 of Lab03
    """Return a string representing the concatenation of the two cities
    that are the answers to puzzle P2"""
    #$ better to define the lists you interator over outside the for loops
    for frenchCity in readWords('words/frenchCities.txt'):
        for italianCity in readWords('words/italianCities.txt'): # for each city in France, we iterate over each city in Italy
            if canon(frenchCity) == canon(italianCity): # if an Italian city is an anagram for a French city, we return their concatenation
                return frenchCity + ' ' + italianCity

def b2(): # for primary extra credit
    """Returns an int representing the number of words that are the
    answer to the puzzle B2"""
    count = 0
    #$ better to define the lists you interator over outside the for loops
    for word in readWords('words/dict.txt'):
        if word.islower() and len(word) == 4 and 'm' in word and uniques(canon(word)) in uniques(canon('mixcent')):
            count += 1 # accumulator increases only if for loop finds lowercase words of length 4 containing 'm' and letters in 'mixcent'
    return count

def p3(): # for another time for fun perhaps
    """Returns a string that is a concatenation of the illness and the name,
    which are the answers to the puzzle P3"""
    pass

if __name__ == '__main__':
    # call puzzle functions
    print("b1(): " + str(b1()))
    print("p1(): " + str(p1()))
    print("p2(): " + str(p2()))
    print("b2(): " + str(b2()))
    print("p3(): " + str(p3()))
