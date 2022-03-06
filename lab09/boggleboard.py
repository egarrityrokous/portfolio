# Boggle board class
"""Extends the Board class with specific features required for Boggle"""

# import modules and classes
from graphics import *
from myrandom import randint
from boggleletter import BoggleLetter
from board import Board

# global variable to represent letters that can go on a boggle cube
CUBES =   [[ "A", "A", "C", "I", "O", "T" ],
           [ "T", "Y", "A", "B", "I", "L" ],
           [ "J", "M", "O", "Qu", "A", "B"],
           [ "A", "C", "D", "E", "M", "P" ],
           [ "A", "C", "E", "L", "S", "R" ],
           [ "A", "D", "E", "N", "V", "Z" ],
           [ "A", "H", "M", "O", "R", "S" ],
           [ "B", "F", "I", "O", "R", "X" ],
           [ "D", "E", "N", "O", "S", "W" ],
           [ "D", "K", "N", "O", "T", "U" ],
           [ "E", "E", "F", "H", "I", "Y" ],
           [ "E", "G", "I", "N", "T", "V" ],
           [ "E", "G", "K", "L", "U", "Y" ],
           [ "E", "H", "I", "N", "P", "S" ],
           [ "E", "L", "P", "S", "T", "U" ],
           [ "G", "I", "L", "R", "U", "W" ]]


class BoggleBoard(Board):
    """Boggle Board class implements the functionality of a Boggle board.
    It inherits from the Board class and extends it by creating a grid
    of BoggleLetters, shaken appropriately to randomize play."""

    __slots__ = ['_grid']

    def __init__(self):
        super().__init__()
        self._grid = [] # we initialize _grid as an empty list
        # we add all of the BoggleLetters in each of the grid boxes to _grid
        for x in range(self.cols):
            colLetters = [BoggleLetter(x, y) for y in range(self.rows)]
            self._grid.append(colLetters)

    def getLetterObj(self, pos):
        """Returns the letter object (that is, a BoggleLetter)
        at given grid position pos, a tuple of (column, row)"""
        col, row = pos # col, row gets the given grid pos
        return self._grid[col][row] # we return BoggleLetter at given grid pos

    def getLetter(self, pos):
        """Returns the text (string) of the BoggleLetter
        at given position pos, a tuple of (column, row)"""
        letObj = self.getLetterObj(pos) # letObj gets Boggleletter at given pos
        return letObj.letter # we return the BoggleLetter as a string

    def setLetter(self, pos, alph):
        """Given grid position pos, a tuple of (column, row),
        set the text of the BoggleLetter at that position to alph (a string)"""
        letObj = self.getLetterObj(pos)
        letObj.letter = alph # we set BoggleLetter to given letter (a string)

    def clearLetters(self):
        """Unclicks all boggle letters on the board without changing any other
        attribute"""
        for x in range(self.cols):
            for y in range(self.rows):
                boggleLetter = self._grid[x][y]
                # for each grid pos, we set BoggleLetter color to 'black' by
                # using .unclick method
                boggleLetter.unclick()

    def reset(self):
        """Clears the boggle board by clearing letters,
        clears all text areas (right, lower, upper) on board
        and resets the letters on board by calling shakeCubes"""

        self.clearLetters() # unclicks all of the boggle letters
        self.clearTextArea() # clears text area
        self.clearLowerText() # clears lower text
        self.clearUpperText() # clears upper text
        self.shakeCubes() # call shakeCubes to randomly reset all BoggleLetters

    def drawBoard(self, win):
        """Draws the boggle board with all the letters on it.
        Overrides inherited drawBoard method of super class"""
        super().drawBoard(win)
        for col in range(self.cols):
            for row in range(self.rows):
                boggleLetter = self._grid[col][row]
                # we draw BoggleBoard with beginning list of BoggleLetters
                boggleLetter.textObj.draw(win)

    def shakeCubes(self):
        """Shakes the boggle board and sets letters
        as described by the handout."""
        l = 0 # accumulator variable
        for col in range(self.cols):
            for row in range(self.rows):
                # for each grid pos, we index into a random row in CUBES that
                # has not already been indexed into
                #$ You don't want to hard code 15 here. Use the define
                #$ self.rows self.cols
                cubeNumber = randint(0, (15-l))
                # in the given row of CUBES we're indexing into, we want to
                # index into a random letter
                sideNumber = randint(0, 5)
                # we set BoggleLetter in each grid pos to random letter in CUBES
                self.setLetter((col,row), CUBES[cubeNumber][sideNumber])
                # we switch row we just indexed into with the last row in CUBES
                CUBES[cubeNumber], CUBES[15-l] = CUBES[15-l], CUBES[cubeNumber]
                # in order to ensure that we don't index into a row in CUBES
                # we've already indexed into, we add 1 to accumulator variable
                l += 1

    def __str__(self):
        """ Returns a string representation of this BoggleBoard """
        board = ''
        # for each box in each column/row, use getter methods for color/letter
        # add string representation of each box (color/letter) to final list
        for c in range(self.cols):
            for r in range(self.rows):
                color = self.getLetterObj((c,r)).color
                letter = self.getLetter((c,r))
                board += '[{}:{}] '.format(letter,color)
            board += '\n'
        return board

if __name__ == "__main__":
    pass
    win = GraphWin("Boggle", 400, 400)
    board = BoggleBoard()
    board.reset()
    board.drawBoard(win)

    exit = False
    while not exit:
        pt = win.getMouse()
        if board.inExit(pt):
            exit = True
        else:
            position = board.getPosition((pt.getX(), pt.getY()))
            print("{} at {}".format(board.getLetter(position), position))
