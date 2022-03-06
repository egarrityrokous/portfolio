# Module provides several functions that are helpful in answering word problems.

"""
This is a module of utilizies for manipulating strings and lists of words.
It consists of several functions, which are helpful in answering word problems
and puzzle questions, especially from NPR and the Spelling Bee from
The New York Times.
"""

__all__ = [ "canon", "uniques", "isIsogram", "readWords", "sized" ]

def letters(phrase):
    """Takes as input a string phrase and returns a string
    that contains just the letters from phrase (in order).

    >>> letters('superb: owl!')
    'superbowl'
    >>> letters('')
    ''
    >>> letters('#@$%')
    ''
    """
    result = ''
    for char in phrase:
        if char.isalpha():  # if char is a letter
            result += char  # concatenate to result
    return result

def canon(word):
    """Takes as input a string word and returns a "canonical" version
    of word: just the letters, in lower case, and in alphabetical order.
    Supports anagram testing.

    >>> canon('fix me') # fix this broken doctest
    'efimx'
    >>> canon('Mamma Mia!')
    'aaaimmmm'
    >>> canon('iAm')
    'aim'
    >>> canon('a lot')
    'alot'
    """
    word = letters(word)      # drop anything that's not a letter (e.g. spaces)
    lowerWord = word.lower()  # to ensure Carol == carol
    orderedWord = sorted(lowerWord) # ie.  a *list* of letters, in alpha order
    result = ''.join(orderedWord) # converts list of letters to a single string
    return result

def uniques(word):
    """Takes as input string word and return a string consisting of the unique
    characters in word.

    >>> uniques('abracadabra')
    'abrcd'
    >>> uniques('Connecticut')
    'Conectiu'
    >>> uniques('$11,003 + $245 = $11,248')
    '$1,03 +245=8'
    >>> uniques('Garrity-Rokous')
    'Garity-Rokus'
    >>> uniques('Alibaba')
    'Aliba'
    """
    result = ''
    for char in word:
        if char not in result: # to ensure result only includes unique characters
            result += char
    return result

def isIsogram(word):
    """Takes as input a string word and returns True only if the
    letters in word are unique (i.e., there are no repeated letters).

    >>> isIsogram('Rita')
    True
    >>> isIsogram('MATH150')
    True
    >>> isIsogram('Bobby')
    False
    >>> isIsogram('STAt201')
    False
    """
    uniqueWord = ''
    lowerWord = uniques(word).lower() # new variable contains only lowercase characters from word
    #$ Do you need this loop?
    for char in lowerWord: # loop adds only unique, lowercase characters to accumulator
        if char not in uniqueWord:
            uniqueWord += char
    if word.lower() == uniqueWord: # returns true if lowercase word is equivalent to accumulator, else false
        return True
    else:
        return False
    #$ can simplify to return word.lower() == lowerWord

def readWords(filename):
    """Takes as input the path to a file filename, opens and reads the words
    (one per line) in that file, and returns a list containing those words.

    >>> len(readWords('words/firstNames.txt'))
    5166
    >>> readWords('words/bodyparts.txt')[14]
    'belly button'
    """
    results = []
    with open(filename) as wordFile:
        for line in wordFile:
            word = line.strip()   # do not use letters (think: 'belly button')
            results.append(word)  # add on to results list
    return results

def sized(n, wordList):
    """Takes as input an integer and a list of strings and returns in a list
    the strings whose lengths are equivalent to the integer.

    >>> sized(4, readWords('words/frenchCities.txt'))
    ['Caen', 'Lyon', 'Metz', 'Nice']
    >>> sized(3, readWords('words/bodyParts.txt'))
    ['arm', 'ear', 'eye', 'hip', 'jaw', 'leg', 'lip', 'toe']
    >>> sized(5, ['kinda', 'cool', 'space', 'face'])
    ['kinda', 'space']
    >>> sized(3, ['who', 'what', 'when', 'why', 'where'])
    ['who', 'why']
    """
    results = []
    for word in wordList:
        if n == len(word):
            results += [word] # if integer equals length of word in wordList, add it to accumulator list
    return results

if __name__ == '__main__':
    # the following code tests the tests in the docstrings ('doctests').
    # as you add tests, re-run this as a script to test your work
    from doctest import testmod  # this import is necessary when testing
    testmod()  # test this module, according to the doctests
