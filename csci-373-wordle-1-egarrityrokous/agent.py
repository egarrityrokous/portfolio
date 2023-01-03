import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from numpy import mean
from random import choice, sample, shuffle
from tqdm import tqdm
from util import read_words, filter_possible_words, get_feedback


def initialize_agent(allowed, possible):
    """Initializes the WordleAgent that game.py uses to play Wordle."""
    return FinalAgent(allowed, possible)

class WordleAgent(ABC):

    def __init__(self, allowed, possible):
        self.allowed = allowed
        self.possible = possible

    @abstractmethod
    def first_guess(self):
        """Makes the first guess of a Wordle game.

        A WordleGame will call this method to get the agent's first guess of the game.
        This is an implicit signal to the agent that a new game has begun. Subsequent
        guess requests during the same game will use the .next_guess method.

        Returns
        -------
        str
            The first guess of a game of Wordle
        """
        ...

    @abstractmethod
    def next_guess(self):
        """Makes the next guess of an in-progress Wordle game.

        A WordleGame will call this method to get the agent's next guess of an
        in-progress game.

        Returns
        -------
        str
            The next guess of the agent, during an in-progress game of Wordle
        """
        ...

    @abstractmethod
    def report_feedback(self, guess, feedback):
        """Provides feedback to the agent after a guess.

        After the agent makes a guess, a WordleGame calls this method to deliver
        feedback to the agent about the guess. No return value is expected from the
        method call.

        Feedback takes the form of a list of colors, corresponding to the letters
        of the guess:
        - "green" means the guessed letter is in the target word, and in the specified position
        - "yellow" means the guessed letter is in the target word, but not in the specified position
        - "gray" means the guessed letter is not in the target word

        For instance, if the WordleGame calls:
            agent.report_feedback("HOUSE", ["gray", "green", "gray", "gray", "yellow"])
        Then the agent can infer that:
            - the target word has the letter "O" in position 2 (counting from 1)
            - the target word contains the letter "E", but not in position 5
            - the target word does not contain letters "H", "U", or "S"
        An example target word that fits this feedback is "FOYER".

        There are some important special cases when the guess contains the same letter in
        multiple positions. Suppose the letter X appears M times in the guess and N times
        in the target:
            - the K appearances of X in a correct position will be "GREEN"
            - if M <= N, then all other appearances of X will be "YELLOW"
            - if M > N, then N-K of the other appearances of X (selected arbitrarily) will
            be "YELLOW". The remaining appearances of X will be "GRAY"

        Parameters
        ----------
        guess : str
            The guess made by the agent
        feedback : list[str]
            A list of colors (expressed as strings "green", "yellow", "gray") corresponding
            to the letters in the guess
        """
        ...

class FinalAgent(WordleAgent):
    best = None # best first guess

    def __init__(self, allowed, possible):
        super().__init__(allowed, possible)
        self.pool = self.possible # poss answers
        self.allow = self.allowed # poss guesses
        self.guess = 0 #num guess

    def partition(self, pool, index, guess):
        """ Takes a set pool and partitions it based on
        the partial feedback it receives (namely the
        info from guess[index])
        """
        guessLett = guess[index]
        green, yellow, gray = [], [], []
        for word in pool:
            if word[index] == guessLett:
                green.append(word)
            elif guessLett in word:
                yellow.append(word)
            else:
                gray.append(word)
        return green, yellow, gray

    def heur(self, guess, pool, i):
        """ Recursive Heuristic for determining whether guess
        is a good guess against a target set pool.
        """
        if len(pool) <= 1 or i == 5: return len(pool) #base cases
        gre, ye, gra = self.partition(pool, i, guess) #partition by info
        greW, yeW, graW, tot = len(gre), len(ye), len(gra), len(pool) # weights
        grePath = (greW/tot) * self.heur(guess, gre, i + 1) # green path
        yePath = (yeW/tot) * self.heur(guess, ye, i + 1) # yellow path
        graPath = (graW/tot) * self.heur(guess, gra, i + 1) # gray path
        return grePath + yePath + graPath # return expected val = weighted sum

    def first_guess(self):
        self.guess = 1
        self.allow = self.allowed
        self.pool = self.possible # reset
        if self.best == None: # only calculate once
            self.best = self.next_guess()
        return self.best

    def next_guess(self):
        if len(self.pool) <= 10 or self.guess == 6: # if pool suff small
            allowed = self.pool
        else: allowed = self.allow
        self.guess += 1
        best = [allowed[0], float('inf')] #best guess, heur val
        for word in allowed:
            value = self.heur(word, self.pool, 0) # calc heuristic
            if value < best[1]: #new best
                best = [word, value]
        return best[0]

    def report_feedback(self, guess, feedback):
        self.pool = filter_possible_words(guess, feedback, self.pool) #filter

class RandomAgent(WordleAgent):
    """A WordleAgent that guesses (randomly) from among words that satisfy the accumulated feedback."""

    def __init__(self, allowed, possible):
        super().__init__(allowed, possible)
        self.pool = self.possible

    def first_guess(self):
        self.pool = self.possible
        shuffle(self.pool)
        return self.next_guess()

    def next_guess(self):
        shuffle(self.pool)
        return self.pool[0]

    def report_feedback(self, guess, feedback):
        self.pool = filter_possible_words(guess, feedback, self.pool)