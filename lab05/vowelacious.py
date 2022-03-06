# Script includes functions with logic errors
"""
This program tests whether or not a word is "vowelacious".  We call
a word vowelacious if it contains 3 or more consecutive vowels.
"""

test1CorrectA = "Eaa" # string is vowelicious; function returns True
test1CorrectB = "Eamon" # string is not vowelicious; function returns False
test1Wrong = "Eaamon" # string is vowelicious; function returns False

test2CorrectA = "Rokouus" # string is vowelicious; function returns True
test2CorrectB = "Rokous" # string is not vowelicious; function returns False
test2Wrong = "Rokouu" # string is vowelicious; function returns False

def isVowelaciousBuggy1(word):
    """Takes a word as input and is supposed to return True if
    the word is vowelacious (contain 3 or more consecutive vowels).
    This version has a logic error.
    TODO: The logic error is not ending the for loop when 3 or more consecutive
    vowels are present in word. It resets the vowel sequence when a consonant
    shows up, even though the vowel sequence may already be 3 consecutive vowels
    long.
    """
    #print('isVowelaciousBuggy1({})'.format(word)) # debugging print
    vowelSeq = '' # initializing variable to accumulate vowel seq

    for char in word:
        if char.lower() in 'aeiou':
            vowelSeq += char # add char
        else:
            vowelSeq = '' # reset if a consonant occurs
        #print('vowelSeq =', vowelSeq) # debugging print

    return len(vowelSeq) >= 3

def isVowelaciousBuggy2(word):
    """Takes a word as input and is supposed to return True if
    the word is vowelacious (contain 3 or more consecutive vowels).
    This version has a logic error.
    TODO: The logic error is the location and use of the elif statement. It
    should beturned into an if statement and indented under the if statement
    above it. That way, the vowel sequence will correctly reset itself when the
    for loop reaches a consonant in word.
    """

    #print('isVowelaciousBuggy2({})'.format(word)) # debugging print
    vowelSeq = '' # initializing variable to accumulate vowel seq
    found = False # initialize return value

    for char in word:
        if char.lower() in 'aeiou':
            vowelSeq += char # add char
        elif len(vowelSeq) >= 3:
            print("Setting found to true") # debugging print.
            #$ comment out debugging prints after solving!
            found = True
        else:
            vowelSeq = '' # reset if a consonant occurs
        #print('vowelSeq =', vowelSeq) # debugging print

    return found

def isVowelacious(word):
    """Takes a word as input and is supposed to return True if
    the word is vowelacious (contain 3 or more consecutive vowels).
    This is the correct version.
    """
    vowelSeq = '' # initializing variable to accumulate vowel seq

    for char in word:
        if len(vowelSeq) >= 3:
            pass # if for loop reaches 3 consecutive vowels, loop ends
        elif char.lower() in 'aeiou':
            vowelSeq += char # add char
        else:
            vowelSeq = '' # reset if a consonant occurs

    return len(vowelSeq) >= 3

if __name__ == "__main__":
    # call the functions on some test cases directly
    #print(isVowelaciousBuggy1("Eamooo"))
    #print(isVowelaciousBuggy2("Rokouu"))
    #print(isVowelacious("Eamooonoo"))
    #$ Make sure to include something in main method so you don't receive an indentation error when running as a script
