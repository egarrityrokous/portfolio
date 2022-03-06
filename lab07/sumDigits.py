"""
Lab 7, Warm-up Task

Fruitful recursion with numbers
sums the digits of a given integer (ignoring its sign)
"""


def sumDigits(num):
    """Given an integer num, computes and returns and integer that is the sum
    of digits of the absolute value of num.
    >>> sumDigits(0)
    0
    >>> sumDigits(-7)
    7
    >>> sumDigits(90)
    9
    >>> sumDigits(-42)
    6
    >>> sumDigits(889832)
    38
    """
    # ignores sign of n
    n = abs(num)

    # base case
    if n < 10:
        return n

    # recursive case
    else:
        lastDigit = n % 10
        #$ To improve readability, want to put whitespace around operators
        #$ consistently.
        sumRest = sumDigits(n // 10) # function calls itself without lastDigit
        return sumRest + lastDigit # returns sum of each digit through recursion
    #$ Good work

#*********************************************************************
#  Testing code in  if __name__=='__main__' block:
#*********************************************************************

if __name__ == '__main__':
    import doctest
    doctest.testmod()
