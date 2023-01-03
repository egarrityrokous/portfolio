import random
import time
from tqdm import tqdm


# Simple 5-bit encodings of the lowercase letters of the English alphabet.
ALPHABETIC_ENCODINGS = {
    'a': '00000', 'b': '00001', 'c': '00010', 'd': '00011', 'e': '00100',
    'f': '00101', 'g': '00110', 'h': '00111', 'i': '01000', 'j': '01001',
    'k': '01010', 'l': '01011', 'm': '01100', 'n': '01101', 'o': '01110',
    'p': '01111', 'q': '10000', 'r': '10001', 's': '10010', 't': '10011',
    'u': '10100', 'v': '10101', 'w': '10110', 'x': '10111', 'y': '11000',
    'z': '11001'
}


def transmit(bitstring, noise_prob):
    """Transmits a bitstring over a noisy channel.

    With probability equal to noise_prob, each bit in the bitstring is flipped during
    transmission (i.e. a "0" will become a "1" and a "1" will become a "0". These
    probabilities are independent.
    """
    def flip(bit):
        return "1" if bit == "0" else "1"
    def transmit_bit(bit):
        return flip(bit) if random.random() < noise_prob else bit
    return ''.join([transmit_bit(bit) for bit in bitstring])


def measure_fidelity(coder, num_trials, noise_prob, show_progress=True):
    """Measures the percentage of transmitted letters that are accurately recovered by a Coder.

    Parameters
    ----------
    coder : coder.Coder
        the Coder that encodes and decodes the transmissions
    num_trials : int
        the number of letters to be transmitted
    noise_prob : float
        the probabilility of any given bit being corrupted (flipped) during transmission
    show_progress : bool
        flag determining whether to show the tqdm progress meter

    Returns
    -------
    float, float
        The accuracy of recovery, and the decoding rate (in letters/second)
    """
    successes, attempts = 0, 0
    decoding_time = 0.0
    letters = list(ALPHABETIC_ENCODINGS.keys())
    trials = tqdm(range(num_trials)) if show_progress else range(num_trials)
    for i in trials:
        letter = letters[i % len(letters)]
        transmission = transmit(coder.encode(letter), noise_prob=noise_prob)
        decoding_start = time.time()
        recovered = coder.decode(transmission)
        decoding_end = time.time()
        decoding_time += decoding_end - decoding_start
        attempts += 1
        if recovered == letter:
            successes += 1
    accuracy = successes / attempts
    decoding_rate = attempts / decoding_time
    return accuracy, decoding_rate
