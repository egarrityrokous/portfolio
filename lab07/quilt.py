"""
Lab 7, Task 2

Non-fruitful recursion.
Using the turtle module, draws a quilt in Williams colors recursively.
"""
from turtle import *

#*********************************************************************
#  Global variables:  Williams colors!
#*********************************************************************
PURPLE = '#8E44AD'
GOLD = '#F4D03F'

### BEGIN HELPER FUNCTIONS ###

def drawSquare(size, color):
    """Draws a single square of side length size (int) and given color (string)
    assuming turtle is initially at one of its endpoints"""
    down()
    pen(fillcolor = color)
    begin_fill()
    for _ in range(4):
        forward(size)
        left(90)
    end_fill()
    up()

def initializeTurtle(size):
    """Setups up the window given size (int) and initializes the turtle to be at
    the bottom left corner of the pattern facing east (the default direction)."""
    padding = 25  # increase if patterns gets cut off
    # Create a turtle window
    setup(width = size + padding, height = size + padding)
    reset() # Clear any existing turtle drawings
            # and reset turtle position & heading.
    up()
    pensize(1) # Choose a pen thickness
    speed(0) # Set the speed; 0=fastest, 1=slowest, 6=normal
    # By default turtle starts at (0,0): center of the screen
    # and by default faces east
    # Put turtle in bottom left corner of the quilt
    goto(-size/2, -size/2)

def testDrawQuilt(size, level, color1=PURPLE, color2=GOLD):
    """Initializes turtle, calls drawQuilt and saves figure"""
    # initialize turtle
    initializeTurtle(size)
    # call drawQuilt
    drawQuilt(size, level, color1, color2)
    # save the figure
    getscreen().getcanvas().postscript(file="drawQuilt-{}-{}.ps".format(size, level))

### END HELPER FUNCTIONS ###

#*********************************************************************
# Draw recursive quilt (Non-fruitful recursion)
#*********************************************************************

def drawQuilt(size, level, color1=PURPLE, color2=GOLD):
    """Draws a colored quilt as described in the lab writeup.
    Assume that the turtle is positioned at the bottom left
    end point of quilt facing east before this function is called.
    """
    if level == 0:
        pass
    else:
        drawSquare(size, color1)
        fd(size/2)
        # assume we are now in middle of bottom of first square turtle draws
        drawQuilt(size/2, level-1, color2, color1)
        bk(size/2)
        lt(90)
        fd(size/2)
        rt(90)

        #$ Inserting a blank line would improve readability as it creates a
        #$ a visual division between the code for the left and right side.
        # assume we are now in middle of left side of first square turtle draws
        drawQuilt(size/2, level-1, color2, color1)
        rt(90)
        fd(size/2)
        lt(90)
        # We are now in our original starting position. Recursion fairy works
        # its magic.
#$ A recursion fairy gets its wings each time a recursion fairy gets its wings

#*********************************************************************
# Testing code given in if __name__ == '__main__' block below
#*********************************************************************

if __name__=='__main__':
    """Testing code"""
    # Uncomment these (one at a time) to test your drawQuint function
    #testDrawQuilt(500, 0) # nothing is drawn
    #testDrawQuilt(500, 1)
    #testDrawQuilt(500, 2)
    #testDrawQuilt(500, 3)
    testDrawQuilt(500, 4)
    #testDrawQuilt(500, 5)
    #testDrawQuilt(500, 6)

    # comment out the line below if you want
    #the turtle screen to close automatically
    #exitonclick()
