"""
This module contains some helper functions for working
with ciphers.  Complete rotateLetter as part of Lab 8.
"""

# add function and variable names that this module provides
__all__ = ['canonical', 'isWord', 'rotateLetter', 'loadStory']

def canonical(word):
    """Takes as input a string word and returns a canonical version of it:
    converts into a lowercase word composed only of letters.

    >>> canonical(' PYTHON!!! ')
    'python'
    """
    # keep only letters, ensuring they're lowercase
    letters = [ letter.lower() for letter in word if letter.isalpha() ]
    return ''.join(letters)

def loadWords(filename='words.txt'):
    """Takes as input the path to a file as string (default is 'words.txt')
    and returns a set of strings containing all the words in file (one per line)

    >>> s = loadWords()
    >>> 'python' in s
    True
    """
    with open(filename) as fin:
        wordSet = {canonical(word) for word in fin} # set comprehension
    return wordSet

def isWord(word, wordSet=loadWords()):
    """Takes as input a word (and optionally a set of words wordSet, by default
    is the set returned by loadWords). Returns true iff a
    canonical version of 'word' is in a wordSet.

    >>> isWord('bat!', {'tan', 'the', 'bat', 'cat'})
    True
    >>> isWord('asdf', {'kind', 'cold', 'beta', 'alpha'})
    False
    >>> isWord('Programmer')
    True
    """
    return canonical(word) in wordSet

def loadStory(filename='story.txt'):
    """Takes as input the path to a file as string (default is 'story.txt'),
    and joins all the lines of the file and returns them as a single string.

    >>> len(loadStory())
    664
    >>> loadStory()[122 : 122 + 4]
    '1821'
    """
    with open(filename) as f:
        story = ' '.join([line.strip() for line in f])
    return story

def rotateLetter(c, n):
    """Takes as input a character c and an int n.  Returns the encryption of
    character c, shifted by n as follows:
    -  Letters are rotated through n places in the alphabet (maintaining case)
    -  Non-letters are returned without change.

    >>> rotateLetter('a', 2)
    'c'
    >>> rotateLetter('a', 26)
    'a'
    >>> rotateLetter('H', 4)
    'L'
    >>> rotateLetter('!', 42)
    '!'
    >>> rotateLetter('z', 29)
    'c'
    >>> rotateLetter('X', 26)
    'X'
    """
    if c.isupper():
        # since ASCII values of cap letters are [65,90] if n shifts c outside of
        # ASCII values of cap letters range, loop around and shift c a total of
        # n places into the beginning of the ASCII values of cap letters range
        if (ord(c) + (n%26)) > 90:
            return chr(64 + (ord(c) + (n%26)) - 90)
            # Shift c by n because it will stay within the ASCII values range of
            # capital letters
        return chr(ord(c) + (n%26))
    elif c.islower():
        # since ASCII values of lowercase letters are [97,122] if n shifts c
        # outside of ASCII values of lowercase letters range, loop around and
        # shift c a total of n places into the beginning of the ASCII values of
        # lowercase letters range
        if (ord(c) + (n%26)) > 122:
            return chr(96 + (ord(c) + (n%26)) - 122)
        # Shift c by n because it will stay within the ASCII values range of
        # lowercase letters
        return chr(ord(c) + (n%26))
        # if c is not a letter, don't shift it and return c
    return c
    #$ You can reduce unneccessary code here by creating variables for the start
    #$and end of the alphabet rather than hard-coding them.

if __name__ == "__main__":
    from doctest import testmod
    testmod()
