"""
Lab 7, Task 1

Accumulating recursion with lists of strings.
Inspired by https://stackoverflow.com/questions/3021/what-is-recursion-and-when-should-i-use-it
"""

def firstSentence(object, subject):
    """Given the strings object and subject, return a string representing the
    first sentence of the story about those characters."""
    return  "The mother of the " + object + " told " + \
            "a story about a " + subject + "..."

def lastSentence(object):
    """Given the string object, return a string representing the second (last)
    sentence of the story about that character."""
    return "and then the " + object + " fell asleep."

def bedtimeStory(characters):
    """
    Main (recursive) function for producing a bedtime story based on a list of
    strings (story characters). Returns a list of strings where each element is
    a sentence in the bedtime story.

    >>> bedtimeStory(['ant', 'fly'])
    ['The mother of the ant told a story about a fly...', 'and then the ant fell asleep.']
    >>> bedtimeStory(['lion'])
    []
    """
    c = characters
    # base case should be an empty list once we recurse over list of characters
    # of length less than 2
    if len(c) < 2:
        return []
    else:
        #$ To improve readability, want to put whitespace around commas
        first = [firstSentence(c[0], c[1])]
        middle = bedtimeStory(c[1:]) # recursive call is already a list
        last = [lastSentence(c[0])]
        # concatenate each list of strings until base case is reached
        return first + middle + last
#$ Nice job
def formatPrint(storyList):
    """Given a list of strings as story list, prints out the full story to the
    terminal in a nicely indented fashion."""
    n = len(storyList)
    for i in range(n):
        currLine = storyList[i]
        if "..." in currLine: #this is a first sentence
            print("   " * i + currLine)
        else: #this is a second sentence
            print(("   " * (n - i - 1)) + currLine)

#*********************************************************************
# Testing code given in if __name__ == '__main__' block below
#*********************************************************************

if __name__ == "__main__":
    """Testing code"""
    from doctest import testmod
    testmod()
    from sys import argv
    chars = argv[1:]
    formatPrint(bedtimeStory(chars))
