# BoggleWord class
"""Implements the functionality of a building and storing words
in the game of Boggle."""

# import boggle letter
from boggleletter import BoggleLetter

class BoggleWords:
    """Implements the functionality of a building and storing words
    in the game of Boggle.
    Uses BoggleLetter class.  Has the following attributes:
    -  _currWord stores current word being constructed and is a list of BoggleLetters
    -  _wordSet is a set of already constructed words.
    -  _allWords is a newline separated strings of constructed words
    """

    __slots__ = ['_currWord', '_wordSet', '_allWords']

    def __init__(self, currWord=[], wordSet=set(), allWords=""):
        """Initializes attributes"""
        self._currWord = currWord
        self._wordSet = wordSet
        self._allWords = allWords

    # getter methods for this class
    @property
    def currWord(self):
        """Returns _currWord attribute of calling object
        """
        return self._currWord

    @property
    def allWords(self):
        """Returns the _allWords attribute of calling object
        """
        return self._allWords

    @property
    def wordStr(self):
        """Returns a string that is the boggle letters in currentWord joined together.
        >>> BoggleWords([BoggleLetter(1, 1, "A"), BoggleLetter(0, 0, "R"), \
BoggleLetter(3, 4, "T")]).wordStr
        'ART'
        """

        currentLetters = [] # accumulator variable
        cW = self.currWord
        # for each BoggleLetter player has clicked on, add it to accumulator
        for letter in cW:
            currentLetters += letter.letter
        # turn accumulator into a string of the letters in BoggleLetter objects
        # that player has clicked on
        return ''.join(currentLetters)

    # following two methods are helpful in adding letters/words during play

    def addLetter(self, nextLetter):
        """Given as input a BoggleLetter, this method appends that letter
        to _currWord attribute.
        """
        self._currWord.append(nextLetter)

    def addWord(self):
        """If currWord being built is not already a word that was added to _wordSet
        then this method adds it to _wordSet, and concatenates it to _allWords
        (with a '\n' as separator)
        """

        # if the string of letters in the BoggleLetter objects player has
        # clicked on so far are not already in the set of words player has
        # found, add it to wordSet and to allWords
        if self.wordStr not in self._wordSet:
            self._wordSet.add(self.wordStr)
            self._allWords += '\n' + self.wordStr

    # following two methods are useful for reset during play

    def clearCurrentWord(self):
        """Resets currWord to be empty"""

        self._currWord = []

    def reset(self):
        """Resets all attributes to empty/initial state."""

        self._currWord = []
        self._wordSet = set()
        self._allWords = ""

    def __str__(self):
        """Print representation of BoggleWords"""

        cW, wS, aW = self.currWord, self._wordSet, self.allWords
        return 'currentWord = {}, wordSet = {}, allWords = {}'.format(cW,wS,aW)

    def __repr__(self):
        """String representation of BoggleWords"""
        #$ Remember that self.curwWord is a list not the string
        cW, wS, aW = self.currWord, self._wordSet, self.allWords
        return 'BoggleWord({}, {}, {})'.format(cW, wS, aW)

if __name__ == "__main__":
    pass
    #from doctest import testmod
    #testmod()

    bw = BoggleWords([], {"CAT", "LAMP"}, "CAT\nLAMP")
    bgl1 = BoggleLetter(0, 0, "A")
    bgl2 = BoggleLetter(0, 1, "R")
    bgl3 = BoggleLetter(1, 0, "M")
    bw.addLetter(bgl1)
    bw.addLetter(bgl2)
    bw.addLetter(bgl3)
    print("before adding word: \n", bw)
    bw.addWord() # should add word "ARM"
    print("after adding word: \n", bw)

    ## if implemented boggle board: try these
    from boggleboard import BoggleBoard
    from graphics import *
    win = GraphWin("Boggle Board", 400, 400)
    bboard = BoggleBoard()
    bboard.drawBoard(win)
    bboard.setTextArea(bw.allWords)

    ## wait for mouse click
    pt = win.getMouse()
