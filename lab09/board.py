'''board.py: The Board class provides a basic game board interface, including
useful methods for creating and manipulating a grid of squares, methods for
converting screen coordinates to grid coordinates and vice versa, and methods
for setting and appending text to various locations outside of the grid.  It
also draws an exit and reset button and provides methods for checking for mouse
clicks inside of those regions.'''

# DO NOT MODIFY

from graphics import *

class Board:
    __slots__ = [ '_xInset', '_yInset', '_rows', '_cols', '_size',\
                '_exitButton', '_resetButton', \
                '_textArea', '_lowerWord', '_upperWord']

    def __init__(self, xInset=50, yInset=50, rows=4, cols=4, size=50):
        self._xInset = xInset       # x inset, avoids drawing in corner of window
        self._yInset = yInset       # y inset, avoids drawing in corner of window
        self._rows = rows           # rows in grid
        self._cols = cols           # columns in grid
        self._size = size           # edge size of each square

        self.__initTextAreas()

    def __initTextAreas(self):
        self._textArea = Text(Point(self.xInset * self.rows + self.size * 2,
                                    self.yInset + 50), "")
        self._textArea.setSize(14)
        self._lowerWord = Text(Point(160, 275), "")
        self._lowerWord.setSize(18)
        self._upperWord = Text(Point(160, 25), "")
        self._upperWord.setSize(18)
        self._upperWord.setTextColor("red")


    def __makeGrid(self, win):
        """Creates a row x col grid, filled with squares"""
        for x in range(self.cols):
            for y in range(self.rows):
                # create first point
                p1 = Point(self.xInset + self.size * x, self.yInset + self.size * y)
                # create second point
                p2 = Point(self.xInset + self.size * (x + 1), self.yInset + self.size * (y + 1))
                r = Rectangle(p1, p2)  # create rectangle
                r.setFill("white")
                r.draw(win) # add rectange to graphical window

    def __makeResetButton(self, win):
        """Add a reset button to board"""
        self._resetButton = Rectangle(Point(50, 300), Point(130, 350))
        self._resetButton.setFill("white")
        self._resetButton.draw(win)
        Text(Point(90, 325), "RESET").draw(win)

    def __makeExitButton(self, win):
        """Add exit button to board"""
        self._exitButton = Rectangle(Point(170, 300), Point(250, 350))
        self._exitButton.draw(win)
        self._exitButton.setFill("white")
        Text(Point(210, 325), "EXIT").draw(win)

    def __drawTextAreas(self, win):
        """Draw the text area to the right/lower/upper side of main grid"""
        self._textArea.draw(win)
        #draw the text area below grid
        self._lowerWord.draw(win)

        #draw the text area above grid grid
        self._upperWord.draw(win)


    def drawBoard(self, win):
        # this creates a row x col grid, filled with squares
        win.setBackground("white smoke")
        self.__makeGrid(win)
        self.__makeResetButton(win)
        self.__makeExitButton(win)
        self.__drawTextAreas(win)


    # getter methods for attributes
    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def size(self):
        return self._size

    @property
    def xInset(self):
        return self._xInset

    @property
    def yInset(self):
        return self._yInset

    # convert grid position to window coordinate
    def _getLocation(self, position):
        '''
        Converts a grid position (tuple) to a window location (tuple).
        Window locations are x, y coordinates.
        '''
        x = position[0] * self.size + self.xInset
        y = position[1] * self.size + self.yInset
        return (x, y)

    # check for click inside specific rectangular region
    def _inRect(self, point, rect):
        '''
        Returns True if a Point (point) exists inside a specific
        Rectangle (rect) on screen.
        '''
        pX = point.getX()
        pY = point.getY()
        rLeft = rect.getP1().getX()
        rTop = rect.getP1().getY()
        rRight = rect.getP2().getX()
        rBottom = rect.getP2().getY()
        return pX > rLeft and pX < rRight and pY > rTop and pY < rBottom

    # check for click in grid
    def inGrid(self, point):
        '''
        Returns True if a Point (point) exists inside the grid of squares.
        '''
        ptX = point.getX()
        ptY = point.getY()
        maxY = self.size * (self.rows + 1)
        maxX = self.size * (self.cols + 1)
        return ptX <= maxX and ptY <= maxY and ptX >= self.xInset and ptY >= self.yInset

    # convert window coordinate (tuple) to grid position (tuple)
    def getPosition(self, location):
        '''
        Converts a window location (tuple) to a grid position (tuple).
        Window locations are x, y coordinates.
        Note: Grid positions are always returned as col, row.
        '''
        if location[1] < self.yInset:
            row = -1
        else:
            row = int((location[1] - self.yInset) / self.size)

        if location[0] < self.xInset:
            col = -1
        else:
            col = int((location[0] - self.xInset) / self.size)
        return (col, row)

    # clicked in exit button?
    def inExit(self, point):
        '''
        Returns true if point is inside exit button (rectangle)
        '''
        return self._inRect(point, self._exitButton)

    # clicked in reset button?
    def inReset(self, point):
        '''
        Returns true if point is inside exit button (rectangle)
        '''
        return self._inRect(point, self._resetButton)

    # set text to text area on right
    def setTextArea(self, text):
        '''
        Sets text to text area to right of grid.
        Overwrites existing text.
        '''
        self._textArea.setText(text)

    # clear text from text area
    def clearTextArea(self):
        '''
        Clear text in text area to right of grid.
        '''
        self._textArea.setText("")

    # add text to text area below grid
    def addStringToLowerText(self, text):
        '''
        Add text to text area below grid.
        Does not overwrite existing text.
        '''
        str = self._lowerWord.getText()
        self._lowerWord.setText( str + text )

    # add text to text area below grid
    def setStringToLowerText(self, text):
        '''
        Set text to text area below grid.
        Overwrites existing text.
        '''
        self._lowerWord.setText( text )

    # clear word below grid
    def clearLowerText(self):
        '''
        Clear text area below grid.
        '''
        self._lowerWord.setText("")

    # set text to text area above grid
    def setStringToUpperText(self, text):
        '''
        Clear text area above grid.
        '''
        self._upperWord.setText(text)

    # clear text above grid
    def clearUpperText(self):
        '''
        Clear text area above grid.
        '''
        self._upperWord.setText("")

if __name__ == "__main__":
    win = GraphWin("Tic Tac Toe", 400, 400)

    # create new board with default values
    board = Board()

    # draw Board
    board.drawBoard(win)
    # set string above grid
    board.setStringToUpperText("Upper text")

    # set and update string below grid
    board.setStringToLowerText("Lower text: ")
    board.addStringToLowerText("D")

    # set string to text area to right of grid
    board.setTextArea("Text area")

    # loop and return info about mouse clicks
    while True:
        # wait for a mouse click
        point = win.getMouse()

        # calculate x and y value from point
        x,y = point.getX(), point.getY()

        # print info about mouse click
        print("Clicked coord {} or grid {}".format((x,y), board.getPosition((x,y))))

        # break and close window if exit is clicked
        if board.inExit(point):
            break
