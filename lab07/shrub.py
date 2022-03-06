"""
Lab 7, Task 3

Fruitful recursion
Implements a module which draws a tree pattern using the Python turtle.
"""
from turtle import *

### BEGIN HELPER FUNCTIONS ###

def initializeTurtle():
    """Setups up the window and initializes the turtle to be at the base of the
    main trunk facing north"""
    setup(600, 600) # Create a turtle window
    reset() # Clear any existing turtle drawings
            # and reset turtle position & heading.
    pensize(1) # Choose a pen thickness
    speed(0) # Set the speed; 0=fastest, 1=slowest, 6=normal
    # By default turtle starts at (0,0): center of the screen
    # and by default faces east
    # set turtle to be roughly off center
    up()
    goto(-100, -200)
    # have it face north
    left(90)
    down()

def testShrub(trunkLength, angle, shrinkFactor, minLength):
    """Initializes turtle, calls shrub and prints returned tuples & saves figure"""
    initializeTurtle()
    numBranches, totLength = shrub(trunkLength, angle, shrinkFactor, minLength)
    print('shrub({}, {}, {}, {}) -> ({}, {})'.format(trunkLength, angle, shrinkFactor,
                              minLength, numBranches, totLength))
    getscreen().getcanvas().postscript(file="shrub-{}-{}-{}-{}.eps".format
                            (trunkLength, angle, shrinkFactor, minLength))

### END HELPER FUNCTIONS ###

#*********************************************************************
# Fruitful Recursive shrub function
#*********************************************************************

def shrub(trunkLength, angle, shrinkFactor, minLength):
    """
    Draws a shrub as specified in Lab 7 Task 3.
    Returns a pair (a 2-tuple) consisting of
      (1) the total number of branches (including the trunk) and
      (2) the total length of the branches (including the trunk) of the shrub.
    Assume that the turtle is positioned at the base of the main
    trunk facing north before this function is called.
    """
    if trunkLength < minLength:
        return (0,0)
    else:
        fd(trunkLength)
        rt(angle)
        newLength1 = trunkLength * shrinkFactor
        # Tuple counts all of the right branches and the total length of all
        # those right branches.
        rCount, rLength = shrub(newLength1, angle, shrinkFactor, minLength)

        #$ Inserting a blank line would improve readability as it creates a
        #$ a visual division between the code for the left and right side.
        # Assume we are now back at the top of the trunk but still facing to the
        # rightward angle. We must now face to the leftward angle.
        lt(2*angle)
        # Left branches should be twice as small as the right branches.
        newLength2 = trunkLength * shrinkFactor * shrinkFactor
        # Tuple counts all of the left branches and the total length of all
        # those left branches.
        lCount, lLength = shrub(newLength2, angle, shrinkFactor, minLength)
        # We must now return to the original point we started at to satisfy the
        # recursion fairy.
        rt(angle)
        bk(trunkLength)

        #$ It would be good to put a space here as well since this is not
        #$ the right or left side, but is a different logical block of code.
        # Return the count of all the branches, including the trunk, and the
        # total length of all the branches, including the trunk, as a tuple.
        return 1 + rCount + lCount, trunkLength + rLength + lLength
#$ Good work. Nice comments

#*********************************************************************
# Testing code given in if __name__ == '__main__' block below
#*********************************************************************

if __name__== '__main__':
    """Testing code"""
    # Uncomment these (one at a time) to test your recursiveSqCount function

    #testShrub(100, 15, 0.8, 60) # should print (4, 308.0)
    #testShrub(100, 15, 0.8, 50) # should print (7, 461.6)
    #testShrub(100, 15, 0.8, 40) # should print (12, 666.4000000000001)
    #testShrub(100, 30, 0.82, 40) # should print (12, 707.95128)
    #testShrub(200, 90, 0.75, 40) # should print (20, 1524.21875)
    testShrub(100, 15, 0.8, 10) # should print (232, 3973.9861913600025)
    #testShrub(100, 30, 0.82, 10) # should print (376, 6386.440567704483)
    #testShrub(200, 90, 0.75, 10) # should print (232, 5056.675148010254)

    # comment out the line below if you want
    #the turtle screen to close automatically
#    exitonclick()
