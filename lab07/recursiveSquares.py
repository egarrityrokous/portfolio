"""
Lab 7, Extra credit

Challenging fruitful graphical recursion problem
"""
from turtle import *

### BEGIN HELPER FUNCTIONS ###

def drawSquare(size, color):
    """Draws a single square of side length size (int) and given color (string)
    assuming turtle is initially at one of its endpoints"""
    pd()
    pen(fillcolor = color)
    begin_fill()
    for _ in range(4):
        fd(size)
        lt(90)
    end_fill()
    pu()

def initializeTurtle(patternSide):
    """Setups up the window and initializes the turtle to be at the bottom left
    corner of the pattern facing east (the default direction)."""
    padding = 25
    setup(width = patternSide + 2*padding, height = patternSide + 2*padding)
    reset() # Clear any existing turtle drawings
            # and reset turtle position & heading.
    pensize(1) # Choose a pen thickness
    speed(0) # Set the speed; 0=fastest, 1=slowest, 6=normal
    # By default turtle starts at (0,0): center of the screen
    # and by default faces east
    # Put turtle in bottom left corner of the quilt
    pu()
    setx(-(patternSide)/2)
    sety(-(patternSide)/2)


def testRecursiveSqCount(patternSide, minSide, color1 = "red", color2 = "blue", color3 = "cyan"):
    """Initializes turtle, calls recursiveSqCount, prints returned tuples & saves figure"""
    # initialize screen and set turtle position to lower left corner of pattern facing east
    initializeTurtle(patternSide)
    # call recursiveSqCount
    c1, c2, c3 = recursiveSqCount(patternSide, minSide, color1, color2, color3)
    # print the tuple returned by recursiveSqCount
    print('recursiveSqCount({}, {})->({}, {}, {})'.format(patternSide, minSide, c1, c2, c3))
    # save the image created as a eps file
    getscreen().getcanvas().postscript(file="recursiveSqCount({},{}).eps".format(patternSide, minSide))

### END HELPER FUNCTIONS ###

#*********************************************************************
# Draw recursive square pattern and count colors (Fruitful recursion)
#*********************************************************************

def recursiveSqCount(patternSide, minSide, color1, color2, color3):
    """Draws a pattern specified in Lab 9 Task 4.
    Returns a triple (a 3-tuple) consisting of
      (1) the total number of squares of color1 in pattern
      (2) the total number of squares of color2 in pattern
      (3) the total number of squares of color3 in pattern
    Assume that the turtle is positioned at the bottom left
    end point of pattern facing east before this function is called.
    """
    if patternSide < minSide:
        return (0, 0, 0)
    else:
        #$ It would be good to have a comment here.
        lt(90)
        fd(patternSide/2)
        rt(90)
        drawSquare(patternSide/2, color1)
        rt(90)
        fd(patternSide/2)
        lt(90)

        #$ Want to chooose more descriptive variable names than c1-c9.  
        #$ You could choose names that distinguish the colors from each of
        #$ the 3 cases.  For example lowerLeft (or ll), upperRight (or up),
        #$ and lowerRight (or lr)
        # assume turtle is back in its original starting position.
        # assign variables to color1, color2, color3 accordingly so they're
        # easy to remember and add up in the end accordingly. Here, c3=color3,
        # c2=color2, c1=colo1
        #$ To improve readability, want to put whitespace around commas
	#$ consistently
        c3, c2, c1 = recursiveSqCount(patternSide/2, minSide, color3, color2, color1)
        fd(patternSide/2)

        #$ It would be good to use blank lines to separate each of the cases
        # assume turtle is now in the middle of the botton of initialized
        # screen. Here, c5=color2, c6=color3, c4=color1.
        c5,c6,c4 = recursiveSqCount(patternSide/2,minSide,color2,color3,color1)
        lt(90)
        fd(patternSide/2)
        rt(90)

        # assume turtle is now in the very center of initialized screen. Here,
        # c9=color3, c7=color1, c8=color2.
        c9,c7,c8 = recursiveSqCount(patternSide/2,minSide,color3,color1,color2)
        bk(patternSide/2)
        rt(90)
        fd(patternSide/2)
        lt(90)

        # assume turtle is now in its original starting position again.
        # recursion fairy works its magic.
        # return 3-item tuple of each number of times a square was drawn in
        # color1, color2, and color3, respectively, by adding up c variables
        # that were previously assigned accordingly. I made sure to add 1 to
        # color1 since the first color1 square drawn would've gone unaccounted
        # for otherwise.
        return 1 + c1 + c4 + c7, c2 + c5 + c8 , c3 + c6 + c9

#$ Nice work here
#*********************************************************************
# Testing code given in if __name__ == '__main__' block below
#*********************************************************************

if __name__ == '__main__':
    """Testing code"""
    pass
    # Uncomment these (one at a time) to test your recursiveSqCount function

    #testRecursiveSqCount(512, 600) #  should print tuple returned as (0, 0, 0)
    #testRecursiveSqCount(512, 512) # should print tuple returned as (1, 0, 0)
    #testRecursiveSqCount(512, 256) # should print tuple returned as (1, 1, 2)
    #testRecursiveSqCount(512, 128) # should print tuple returned as (6, 4, 3)
    #testRecursiveSqCount(512, 64) # should print tuple returned as (11, 13, 16)
    testRecursiveSqCount(512, 32) # should print tuple returned as (46, 40, 35)
    #testRecursiveSqCount(512, 16) # should print tuple returned as (111, 121, 132)

    # Warning: the following call takes way too long to finish
    #testRecursiveSqCount(512, 8) # should print tuple returned as (386, 364, 343)

    # uncomment line below if you don't want turtle screen to close automatically
    #exitonclick()
