### Lab 2:  Computing the Day of the Week

In this lab, you will write a script `day.py` which computes
the day of the week.


You can find the PDF of the lab handout on the course webpage: 
* http://cs.williams.edu/~cs134/labs-and-hws.html 

This lab's starter files:
* GradeSheet.txt - rubric for this lab's grading	
* README.md - this file	
* day.py - script you will write in this lab	
* honorcode.txt - the honor code pledge, to be signed.


When run as a script, `day.py` prints the current day of the week in Williamstown.

When imported, it provides three functions:
 * UTCDay(timeval) - returns wday (0 = Sun) associated w/timeval in London (UTC+0)
 * localDay(timeval, offset) - returns wday associated w/timeval,
                               and timezone specificed by offset in hours
			       (Williamstown = -5)
 * dayOfWeek(wday) - returns wday as str: 0 => 'Sunday', 1 => 'Monday', etc


