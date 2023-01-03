from abc import ABC, abstractmethod
import argparse
import random
import time
from tqdm import tqdm
from util import ALPHABETIC_ENCODINGS
from collections import defaultdict
from inference import Factor, BayesianNetwork, run_inference
import copy


def initialize_coder(noise_prob):
    """Initializes the Coder that turbo.py uses to encode and decode transmissions.

    CHANGE THIS FUNCTION TO INITIALIZE YOUR OWN CODERS.

    """
    return MyImprovedCoder(noise_prob)


class Coder(ABC):
    """
    A Coder is responsible for encoding and decoding lowercase alphabetic letters.

    The .encode method is responsible for converting a lowercase alphabetic letter
    into a string of 15 bits (represented as a Python string of zeroes and ones).

    The .decode method is responsible for converting a string of 15 bits into a
    lowercase alphabetic letter. It is assumed that the bitstring was initially created
    using the .encode method, and then was "transmitted" with a bit corruption probability
    of self.noise_prob -- i.e. each bit is flipped during transmission (0 becomes 1,
    and 1 becomes 0) with a probability of self.noise_prob. These probabilities are
    independent.
    """

    def __init__(self, noise_prob):
        """
        Parameters
        ----------
        noise_prob : float
            The probability of a bit corruption.
        """
        self.noise_prob = noise_prob

    @abstractmethod
    def encode(self, letter):
        """Converts a lowercase alphabetic letter into a string of 15 bits.

        Parameters
        ----------
        letter : str
            The lowercase letter, represented as a string of length 1

        Returns
        -------
        str
            A string of length 15, consisting exclusively of zeroes and ones
        """

    @abstractmethod
    def decode(self, bitstring):
        """Converts a string of 15 bits into a lowercase alphabetic letter.

        It should be assumed that the bitstring was initially created using the .encode
        method, and then was "transmitted" with a bit corruption probability
        of self.noise_prob -- i.e. each bit was flipped during transmission (0 becomes 1,
        and 1 becomes 0) with a probability of self.noise_prob. These probabilities are
        independent.

        Parameters
        ----------
        bitstring : str
            A string of length 15, consisting exclusively of zeroes and ones

        Returns
        -------
        str
            The lowercase letter, represented as a string of length 1
        """


class NaiveCoder(Coder):
    """A NaiveCoder just encodes a letter by appending 10 zeroes to its 5-bit encoding.

    Decoding is therefore simple: the 10 trailing zeroes are ignored and the first 5 bits
    are interpreted as the letter that they correspond to. If the first 5 bits don't correspond
    to any letter (due to bit corruption), then the bitstring is arbitrarily interpreted
    as the letter "x".
    """

    def __init__(self, noise_prob):
        super().__init__(noise_prob)
        self.alphabetic_encoding_inverted = {v: k for (k, v) in ALPHABETIC_ENCODINGS.items()}

    def encode(self, letter):
        """Appends 10 zeroes to the 5-bit encoding of the letter."""
        encoding = ALPHABETIC_ENCODINGS[letter]
        return encoding + "0000000000"

    def decode(self, bitstring):
        """Uses the first 5 bits of the bitstring to interpret the bitstring.

        The 10 trailing zeroes are ignored and the first 5 bits are interpreted as the
        letter that they correspond to. If the first 5 bits don't correspond to any
        letter (due to bit corruption), then the bitstring is arbitrarily interpreted
        as the letter "x".
        """
        if bitstring[:5] in self.alphabetic_encoding_inverted:
            return self.alphabetic_encoding_inverted[bitstring[:5]]
        else:
            return "x"


class TriplicateCoder(Coder):
    """A TriplicateCoder encodes a letter by concatenating its 5-bit encoding three times.

    You must write the .decode method by implementing a Bayesian network that computes
    the most probable letter, given the received bitstring.
    """

    def __init__(self, noise_prob):
        super().__init__(noise_prob)

    def encode(self, letter):
        """Concatenates the 5-bit encoding of the letter three times."""
        encoding = ALPHABETIC_ENCODINGS[letter]
        return encoding + encoding + encoding

    def decode(self, bitstring):
        """Computes the most probable original letter, given the received bitstring."""
        factors = []

        # create factors for received bit variables
        received_variables = [[f"R{i}", f"T{i}"] for i in range(1, 16)]
        received_values_template = {
            ("0", "0"): (1-self.noise_prob),
            ("0", "1"): self.noise_prob,
            ("1", "0"): self.noise_prob,
            ("1", "1"): (1-self.noise_prob),
        }
        received_values = [copy.deepcopy(received_values_template) for _ in range(15)]
        factors.extend([Factor(variables, values) for variables, values in zip(received_variables, received_values)])

        # create factors for transmitted bit variables
        transmitted_variables = [[f"T{i+1}", f"M{(i%5) + 1}"] for i in range(0, 15)]
        transmitted_values_template = {
            ("0", "0"): 1.0,
            ("0", "1"): 0.0,
            ("1", "0"): 0.0,
            ("1", "1"): 1.0,
        }
        transmitted_values = [copy.deepcopy(transmitted_values_template) for _ in range(15)]
        factors.extend([Factor(variables, values) for variables, values in zip(transmitted_variables, transmitted_values)])

        # create factors for message bit variables
        message_variables = [[f"M{i}", "A"] for i in range(1, 6)]
        message_values = []
        for i in range(5):
            # m_dict stores 26*2=52 items: (0, {letter}) and (1, {letter}) for each letter.
            m_dict = dict()
            for letter, encoding in ALPHABETIC_ENCODINGS.items():
                m_dict[("0", letter)] = float(encoding[i] == "0")  # value is 1.0 if encoding[i] == 0, otherwise 0.0
                m_dict[("1", letter)] = float(encoding[i] == "1")  # value is 1.0 if encoding[i] == 1, otherwise 0.0
            message_values.append(m_dict)
        factors.extend([Factor(variables, values) for variables, values in zip(message_variables, message_values)])

        # create factor for letter variable
        alphabet_variables = ["A"]
        alphabet_values = {(letter,): 1/26 for letter in ALPHABETIC_ENCODINGS.keys()}
        factors.append(Factor(alphabet_variables, alphabet_values))

        domains = {}
        for i in range(1, 16):
            domains[f"R{i}"] = ["0", "1"]
            domains[f"T{i}"] = ["0", "1"]
        for i in range(1, 6):
            domains[f"M{i}"] = ["0", "1"]
        domains["A"] = list(ALPHABETIC_ENCODINGS.keys())

        # create Bayes net
        b_net = BayesianNetwork(factors, domains)

        # observed evidence is the received bits
        evidence = {f"R{i+1}": bit for i, bit in enumerate(list(bitstring))}

        # compute P(v | evidence) for all variables
        res = run_inference(b_net, evidence)
    
        # list of (probability, letter) indicating estimated likelihood that the bitstring encodes letter
        probs = [(res["A"].get_value({"A": letter}), letter) for letter in ALPHABETIC_ENCODINGS.keys()]
        return max(probs)[1]


class MyImprovedCoder(Coder):
    """Encodes/decodes letters using your improved Bayesian network-based protocol."""

    def __init__(self, noise_prob):
        super().__init__(noise_prob)


    def encode(self, letter):
        """Converts a lowercase alphabetic letter into a string of 15 bits, according to your protocol.

        Encoding:
        T1 T2 T3 T4 T5  T6     T7     T8     T9     T10    T11    T12    T13    T14    T15
        M1 M2 M3 M4 M5  M1^M2  M1^M3  M2^M3  M2^M4  M3^M4  M3^M5  M4^M5  M4^M1  M5^M1  M5^M2
        """
        encoding = ALPHABETIC_ENCODINGS[letter]
        result = ""
        result += encoding
        message_list = [(1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,5), (4,1), (5,1), (5,2)]
        for (a,b) in message_list:
            first = int(encoding[a-1])
            second = int(encoding[b-1])
            result += str(first ^ second)
        
        return result

    def decode(self, bitstring):
        """Computes the most probable original letter, given the received bitstring."""
        factors = []

        # create factors for received bit variables
        received_variables = [[f"R{i}", f"T{i}"] for i in range(1, 16)]
        received_values_template = {
            ("0", "0"): (1-self.noise_prob),
            ("0", "1"): self.noise_prob,
            ("1", "0"): self.noise_prob,
            ("1", "1"): (1-self.noise_prob),
        }
        received_values = [copy.deepcopy(received_values_template) for _ in range(15)]
        factors.extend([Factor(variables, values) for variables, values in zip(received_variables, received_values)])

        # create factors for first 5 transmitted bit variables (no XOR used)
        simple_transmitted_variables = [[f"T{i+1}", f"M{(i%5) + 1}"] for i in range(0, 5)]
        simple_transmitted_values_template = {
            ("0", "0"): 1.0,
            ("0", "1"): 0.0,
            ("1", "0"): 0.0,
            ("1", "1"): 1.0,
        }
        simple_transmitted_values = [copy.deepcopy(simple_transmitted_values_template) for _ in range(15)]
        factors.extend([Factor(variables, values) for variables, values in zip(simple_transmitted_variables, simple_transmitted_values)])

        # create factors for last 10 transmitted bit variables (those using XOR)
        message_list = [(1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,5), (4,1), (5,1), (5,2)]
        xor_transmitted_variables = []
        t_counter = 6
        for (a,b) in message_list:
            first = "M" + str(a)
            second = "M" + str(b)
            t_var = "T" + str(t_counter)
            t_counter += 1
            xor_transmitted_variables.append([t_var,first,second])

        xor_transmitted_values_template = {
            ("0", "0", "0"): 1.0,
            ("0", "1", "0"): 0.0,
            ("0", "0", "1"): 0.0,
            ("0", "1", "1"): 1.0,
            ("1", "0", "0"): 0.0,
            ("1", "1", "0"): 1.0,
            ("1", "0", "1"): 1.0,
            ("1", "1", "1"): 0.0,
        }

        xor_transmitted_values = [copy.deepcopy(xor_transmitted_values_template) for _ in range(10)]
        factors.extend([Factor(variables, values) for variables, values in zip(xor_transmitted_variables, xor_transmitted_values)])

        # create factors for message bit variables
        message_variables = [[f"M{i}", "A"] for i in range(1, 6)]
        message_values = []
        for i in range(5):
            # m_dict stores 26*2=52 items: (0, {letter}) and (1, {letter}) for each letter.
            m_dict = dict()
            for letter, encoding in ALPHABETIC_ENCODINGS.items():
                m_dict[("0", letter)] = float(encoding[i] == "0")  # value is 1.0 if encoding[i] == 0, otherwise 0.0
                m_dict[("1", letter)] = float(encoding[i] == "1")  # value is 1.0 if encoding[i] == 1, otherwise 0.0
            message_values.append(m_dict)
        factors.extend([Factor(variables, values) for variables, values in zip(message_variables, message_values)])

        # create factor for letter variable
        alphabet_variables = ["A"]
        alphabet_values = {(letter,): 1/26 for letter in ALPHABETIC_ENCODINGS.keys()}
        factors.append(Factor(alphabet_variables, alphabet_values))

        domains = {}
        for i in range(1, 16):
            domains[f"R{i}"] = ["0", "1"]
            domains[f"T{i}"] = ["0", "1"]
        for i in range(1, 6):
            domains[f"M{i}"] = ["0", "1"]
        domains["A"] = list(ALPHABETIC_ENCODINGS.keys())

        # create Bayes net
        b_net = BayesianNetwork(factors, domains)

        # observed evidence is the received bits
        evidence = {f"R{i+1}": bit for i, bit in enumerate(list(bitstring))}

        # compute P(v | evidence) for all variables
        res = run_inference(b_net, evidence)
    
        # list of (probability, letter) indicating estimated likelihood that the bitstring encodes letter
        probs = [(res["A"].get_value({"A": letter}), letter) for letter in ALPHABETIC_ENCODINGS.keys()]
        return max(probs)[1]
