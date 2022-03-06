"""Running this code as a script decrypts the mystery message
contained in file 'story.txt'.  Uses cipherClasses and cipherTools modules"""

# import relevant classes
from cipherClasses import *

# import helper functions
from cipherTools import *


if __name__ == "__main__":
    # story gets object of Message class that is meant to be decrypted
    story = Ciphertext(loadStory('story.txt'))
    # decryptedStory gets the decrypted message of story with the most real
    # words (i.e. the best version of the decrypted message)
    decryptedStory = story.bestDecryption
    # outputs the decrypted story as a single string
    print(decryptedStory)
