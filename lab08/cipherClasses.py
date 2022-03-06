"""
This module includes three useful class definitions that help with shifting text
through the alphabet and counting words, encrypting text, and decrypting text,
respectively.
"""

# import helper functions
from cipherTools import *

# The following items might be useful to others:
__all__ = ['Plaintext', 'Ciphertext']

class Message:
    """Objects of this class hold text strings and have methods that can shifts
    text through the alphabet and count words.
    """
    __slots__ = ['_text']

    def __init__(self, text=''):
        """Builds a Message with given text.

        >>> Message('The snake arrived.')._text
        'The snake arrived.'
        >>> Message('Hello, world1!')._text
        'Hello, world1!'
        >>> Message('I love Ephs.')._text
        'I love Ephs.'
        """
        self._text = text

    @property
    def text(self):
        """Returns self.text.
        Used to safely access self._text

        >>> Message('Fall in MA means snow.').text
        'Fall in MA means snow.'
        >>> Message('').text
        ''
        >>> Message('CS is the greatest major!').text #$ :-)
        'CS is the greatest major!'
        """
        return self._text

    @property
    def wordCount(self):
        """Returns the number of dictionary words found in the Message,
        when split up by spaces.

        >>> msg = Message("Hello, world!")
        >>> msg.wordCount
        2
        >>> Message("Who hates covid-19?").wordCount
        2
        >>> Message("It's as easy as 123, ABC!").wordCount
        4
        >>> Message("").wordCount
        0
        >>> Message("Charlie and Eamon").wordCount
        1
        """
        text = self.text.split() # separates text into a list of each word
        answer = 0 # accumulator variable
        for word in text:
            # isWord only looks at the letters in the word and checks if word is
            # in the English dictionary
            if isWord(word):
                answer += 1
        return answer # returns word count
        #$ Good work.

    def rotate(self, shift):
        """Returns a string with the Message's text, but with letters
        rotated by 'shift' characters.  Shift should be zero or greater.

        >>> Message('Cheer').rotate(7)
        'Jolly'
        >>> Message('2001: IBM').rotate(25)
        '2001: HAL'
        >>> Message('123, AbC!').rotate(32)
        '123, GhI!'
        >>> Message('Ticker = AAPL').rotate(4)
        'Xmgoiv = EETP'
        """
        rotatedString = '' # accumulator string
        for letter in self.text:
            # rotates each letter of the word and concatenates it to accumulator
            rotatedString += rotateLetter(letter, shift)
        return rotatedString # returns correctly shifted word
        #$ Good work. Very clear

    def __str__(self):
        """Convert Message to a string

        >>> str(Message('Hello, world!'))
        'Hello, world!'
        >>> print(Message('Print me.'))
        Print me.
        >>> str(Message('Caesar cipher'))
        'Caesar cipher'
        """
        return self.text

    def __repr__(self):
        """Generate a representation of Message

        >>> repr(Message('Hello, world!'))
        'Message("Hello, world!")'
        >>> repr(Message('battleship'))
        'Message("battleship")'
        """
        return 'Message("{}")'.format(self.text)

class Plaintext(Message):
    """Inherits attributes of Message class and takes objects of it that are
    meant to be encrypted. These objects keep track of a shift count and can
    encrypt the plaintext.
    """
    __slots__ = ['_shift']

    def __init__(self, text='', shift=0):
        """Builds a Plaintext object, based on text (a string) and a
        desired shift amount (a non-negative integer).

        A Plaintext supports several properties:
            self.text  (plain text, inherited from Message, a string)
            self.wordCount (the count of words, inherited from Message, an int)
            self.shift (amount of rotation, an integer)
            self.encrypt (encrypted text, a string)

        >>> p = Plaintext('mellon', 16)
        >>> p._shift
        16
        >>> p._text
        'mellon'
        >>> Plaintext('123, AbC!')._shift
        0
        >>> Plaintext('123, AbC!', -1)._shift
        -1
        >>> Plaintext('', 28)._text
        ''
        >>> Plaintext('docking, docks, dockyard').wordCount
        3
        """
        super().__init__(text) # calls the initializer for Message
        self._shift = shift # includes shift in Plaintext attributes

    @property
    def shift(self):
        """Returns the shift amount.

        >>> Plaintext('HAL', 1).shift
        1
        >>> Plaintext('123, aBC!', -1).shift
        -1
        >>> Plaintext('123, aBC!').shift
        0
        >>> Plaintext('Large Shift', 420).shift
        420
        """
        return self._shift

    @shift.setter
    def shift(self, shiftValue):
        """Changes the shift value associated with this message.
        The shiftValue should not be negative.  Notice that shifting
        by a shiftValue of 26 or more is the same as
        shifting by shiftValue%26.

        >>> msg = Plaintext('hello', 12)
        >>> msg.shift = 3
        >>> msg.shift
        3
        >>> msg = Plaintext('123, aBC!', 28)
        >>> msg.shift = 0
        >>> msg.shift
        0
        >>> msg = Plaintext('aardvark', 999)
        >>> msg.shift = 998
        >>> msg.shift
        998
        """
        # allows you to change the value of shift on the fly
        self._shift = shiftValue #$ % 26 (see docstring above)

    @property
    def encrypt(self):
        """Returns a string that is the encrypted version of this plaintext
        message, based on the current shift amount.

        >>> msg = Plaintext('hello', 2)
        >>> msg.encrypt
        'jgnnq'
        >>> Plaintext('123, aBC!', 32).encrypt
        '123, gHI!'
        >>> Plaintext('oompa loompa', 12).encrypt
        'aaybm xaaybm'
        """
        # returns and rotates letters of plaintext message by given shift value
        # and returns this encrypted message as a string
        return self.rotate(self.shift)
        #$ Nice work. I like the doctest.

    def __repr__(self):
        """Generate a representation of Plaintext

        >>> repr(Plaintext('Hello, world!', 2))
        'Plaintext("Hello, world!", 2)'
        >>> repr(Plaintext('Airline Pilot', 13))
        'Plaintext("Airline Pilot", 13)'
        """
        return 'Plaintext("{}", {})'.format(self.text, self.shift)

class Ciphertext(Message):
    """Takes objects of Message class that are meant to be encrypted and
    supports manual and automatic decryption into Plaintext objects. Also
    inherits attributes of Message class.
    """
    __slots__ = []

    def __init__(self, text=''):
        """Builds a new CipherText object for holding encrypted text (string).

        A Ciphertext object supports the following properties:
            self.text (the ciphertext, ideally inherited from Message, a string)
            self.wordCount (the count of words in the cipher, inherited, an int)

        >>> Ciphertext('jgnnq').text
        'jgnnq'
        >>> Ciphertext('jgnnq').wordCount
        0
        >>> Ciphertext('EaSy aS 123, AbC!').text
        'EaSy aS 123, AbC!'
        >>> Ciphertext('EaSy aS 123, AbC!').wordCount
        2
        >>> Ciphertext('Jackson 5').wordCount
        1
        """
        super().__init__(text) # calls the initializer for Message

    def decrypt(self, unshift):
        """Generates and returns the Plaintext associated with shifting
        *backwards* by unshift, an integer.  Notice that shifting backwards is
        the same as shifting forward by 26 - unshift.

        >>> plain = Ciphertext('jgnnq').decrypt(2)
        >>> plain.text
        'hello'
        >>> plain.wordCount
        1
        >>> Ciphertext('123, AbC!').decrypt(28).text
        '123, YzA!'
        >>> Ciphertext('Zmfuazmx Fdqmegdq').decrypt(12).text
        'National Treasure'
        """
        # since shifting backwards is the same as shifting forwards by 26 -
        # unshift, we want to make sure shift gets the value of 26 - unshift
        shift = 26 - unshift
        # returns the Plaintext, decrypted message based on given unshift value
        return Plaintext(self.rotate(shift), shift)
        #$ return Plaintext(self.rotate(shift),unshift)

    @property
    def bestDecryption(self):
        """Returns a Plaintext object that is the best decryption of this
        message. The 'best' description has the largest number of words in the
        resulting Plaintext.

        >>> plain = Ciphertext('jgnnq').bestDecryption
        >>> plain.text
        'hello'
        >>> Ciphertext('GcUa cU 123, CdE!').decrypt(28).text
        'EaSy aS 123, AbC!'
        >>> plain = Ciphertext('Fqumf Hjsyfzwn').bestDecryption
        >>> plain.text
        'Alpha Centauri'
        """
        numWords = 0 # accumulator variable
        for i in range(27): # for integer in range of length of the alphabet + 1
            decipher = self.decrypt(i) # decipher gets current decrypted message
            # if the number of words in the current decrpyted mesage is the
            # greater than the last decrypted message, increase the accumulator
            # variable by 1 and bestDecipher gets the current decrypted message
            # with the most real words in it
            if decipher.wordCount >= numWords:
                numWords += 1
                bestDecipher = decipher
        # returns the best (i.e. having the most real words) decrypted message
        return bestDecipher
        #$ numWords should not be an accumulator variable. It should keep track
        #$ of the wordCount of the best message you have found so far.

    def __repr__(self):
        """Generate a representation of Ciphertext

        >>> repr(Ciphertext('jgnnq'))
        'Ciphertext("jgnnq")'

        >>> repr(Ciphertext('Grade A Eggs'))
        'Ciphertext("Grade A Eggs")'

        """
        return 'Ciphertext("{}")'.format(self.text)

# Only run when code is run as a script:
if __name__ == '__main__':
    from doctest import testmod
    testmod()
