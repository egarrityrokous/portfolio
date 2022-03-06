# Compute and print the current day of the week.

# import module to compute the seconds since midnight of 1/1/1970:
from time import time

def UTCDay(timeval):
    """Takes as input UTC time value (float), and returns the
    number of the day of the week (integer between 0 and 6 inclusive)"""
    #$ We want to make lines of code plus comments don't exceed 80 chars (the
    #$ gray vertical line in Atom). If the comment would exceed the line limit,
    #$ move it to a line preceding the line of code it's describing.
    # timeval is converted into an integer, adjusted to the number of seconds since Sunday, January 4, 1970, and then converted to the number of days since then.
    # at the end of the body, the remainder, corresponding to a certain day of the week, of timeval divided by 7 is returned.
    timeval = int(timeval)
    #$ To improve readability, it's good to surround operators with whitespace
    #$ as you have done in a number of places.  You want to do it consistently.
    #$ Meaning, you should have spaces around the multiplication operator too.
    timeval = timeval - (3*3600*24) #$ Try to space out operators
    timeval = timeval // 3600 // 24
    return timeval % 7

def localDay(timeval, offset):
    """Takes as input UTC time value  (float) and an offset (float),
    calls UTCDay to help compute the current day of the week
    for a timezone that is offset hours ahead of UTC."""
    #$ Try not to let lines exceed 80 chars, including comments
    # timeval is converted to an integer, converted to hours and adjusted for the timezone, and then converted back into seconds.
    # timeval is then run through the UTCDay function, defined above.
    timeval = int(timeval)
    timeval = (timeval // 3600) + offset
    timeval = timeval * 3600 #$ Can avoid this line by simply adding offset * 3600
    return (UTCDay(timeval))

def dayOfWeek(day):
    """Takes an integer between 0 and 6 (inclusive) as input and
    returns the name of that day as a string"""
    #$ Try not to let lines exceed 80 chars, including comments
    # if the input for day corresponds to a certain day of the week, a string for that day of the week is returned.
    if day == 0:
        return 'Sunday'
    elif day == 1:
        return 'Monday'
    elif day == 2:
        return 'Tuesday'
    elif day == 3:
        return 'Wednesday'
    elif day == 4:
        return 'Thursday'
    elif day == 5:
        return 'Friday'
    elif day == 6:
        return 'Saturday'
    #$ What would happen if the user entered 7?  We want to make sure an
    #$ answer is returned regardless of what the user enters.

if __name__ == "__main__": # run as a script
    # statements in this suite are only executed when this is run as a script:
    now = time() # UTC time
    dayNumber = localDay(now, -4) # Eastern day of week number
    dayName = dayOfWeek(dayNumber) # get day name
    print("It's " + dayName + "!") # print it out
