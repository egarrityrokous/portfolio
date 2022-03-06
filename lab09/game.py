# script game.py
"""Implements the logic of the game of boggle."""

# import all relevant packages and classes
from graphics import *
from random import randint
from boggleboard import BoggleBoard
from boggleletter import BoggleLetter
from bogglewords import BoggleWords
import time

# This helper function creates the Boggle lexicon.
def lexicon(filename='bogwords.txt'):
    """Reads words (one per line) from filename (by default 'bogwords.txt')
    and returns a set of all words"""
    result = set()
    with open(filename) as f:
        for lines in f:
            result.add(lines.strip())
    return result

# This helper function sets and can help reset the timer for the Boggle game.
#$ added board to parameters of setTimer to get testing to work
#$ should be passed to function since board is not a global variable!
def setTimer(startTime, currentTime, seconds, board):
    """Given a start time, the current time, and a number of seconds, this
    function sets a timer for the game at the top of the BoggleBoard graphical
    window and can be used to help reset the timer as well."""

    # calculate difference between startTime and CurrentTime
    difference = currentTime - startTime
    timeLeft = int(seconds - difference) # calculate time left for timer
    time.sleep(.1) # code waits for .1 second before continuing
    # set timer to top of the screen in red, counting down seconds from 180
    if timeLeft > 0: # if timer is greater than 0, keep counting down
        board.setStringToUpperText('Timer: {}'.format(timeLeft))
    else: # if timer reaches 0, let player know time is up
        board.setStringToUpperText('Time is up!')

def setup(win, board):
    """Given a graphical window and BoggleBoard board,
    sets up the game board by resetting the letters on it
    and drawing the board with letters"""

    board.drawBoard(win) # draws the board on the graphical window
    board.reset() # resets the board with all the letters on it

def resetLower(board):
    """Given a BoggleBoard board, clears the letters on the board,
    along with the lower text area"""

    board.clearLetters() # unclicks all of the letters
    board.clearLowerText() # clears the lower text area

def update(board, bWords):
    """Updates the state of the BoggleBoard board after a valid word has been
    found and added to BoggleWords bWords; updates right text area, clears lower
    text area, and resets BoggleLetters to unclicked state."""

    # sets right text area to all words found so far
    board.setTextArea(bWords.allWords)

    board.clearLowerText() # clears text under grid
    board.clearLetters() # unclicks all letters on the board
    bWords.clearCurrentWord() # clears current word player is trying to find

def play(win, board):
    """Given a graphical window and a BoggleBoard board, implements the logic
    for playing the game"""

    # initialize flag and boggle words
    exitFlag = False

    # populate the lexicon
    validWords = lexicon()

    # initialize an empty BoggleWords object
    bWords = BoggleWords()

    # initialize number of seconds to play the game
    seconds = 10

    # initialize the start time for the game
    startTime = time.time()

    while not exitFlag:

        # initialize the current time in the game
        currentTime = time.time()

        # find (col, row) coord of mouse click
        point = win.checkMouse()

        # check for mouse click and go through steps of Boggle game logic
        if point:

            # step 1: check for exit button and exit
            if board.inExit(point):
                exitFlag = True

            # step 2: check for reset button, reset state, and reset timer
            elif board.inReset(point):
                startTime = time.time()
                board.reset()
                bWords.clearCurrentWord()
                bWords.reset()

            # step 3: check if click is on a cell in the grid
            elif board.inGrid(point):

                # get BoggleLetter at that position
                position = board.getPosition((point.getX(), point.getY()))
                boggleLetter = board.getLetterObj(position)

                # if starting new word, add letter and display it on lower text
                # of board and turn letter blue.
                if len(bWords.currWord) == 0:
                    bWords.addLetter(boggleLetter)
                    boggleLetter.click()
                    board.addStringToLowerText(bWords.wordStr[-1])

                # if adding letter to existing word, check for adjacency,
                # update state.
                else:
                    #$ Missing check if letter is clicked previously. Right now,
                    #$ you can select the same letter multiple times
                    #$ Timer also don't stop the game
                    if boggleLetter.isAdjacent(bWords.currWord[-1]):
                        # if last letter clicked is adjacent to letter clicked
                        # before that, set former to blue and latter to green
                        # and add former to currWord and to lowerText
                        bWords.currWord[-1].color = 'green'
                        bWords.addLetter(boggleLetter)
                        boggleLetter.click()
                        board.addStringToLowerText(bWords.wordStr[-1])

                # if clicked on same letter as last time, check for validity
                # and then end the word. If word is valid, add it to bWords and
                # update bWords; else, reset state.
                    else:
                        if boggleLetter == bWords.currWord[-1]:
                            if bWords.wordStr.lower() in validWords:
                                bWords.addWord()
                                update(board, bWords)
                            else:
                                update(board, bWords)

                # if clicked on some other letter, cancel word, reset state.
                        else:
                            update(board, bWords)

        # account for when win.checkMouse() == None
        else:
            # start the timer and put it at the top of the window
            setTimer(startTime, currentTime, seconds, board)


if __name__ == '__main__':
    pass
    win = GraphWin("Boggle", 400, 400)
    board = BoggleBoard()
    setup(win, board)
    play(win, board)
