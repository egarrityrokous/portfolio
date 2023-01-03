import unittest
from coder import initialize_coder
from util import measure_fidelity

class TestOne(unittest.TestCase):

    def test_noise_0_1(self):
        try:
            noise_prob = 0.1
            num_transmissions = 2000
            encoder = initialize_coder(noise_prob)
            accuracy, rate = measure_fidelity(encoder, num_transmissions, noise_prob,
                                              show_progress=False)
            print("\n-------------------------------------------------------")
            print(f"With a bit corruption probability of 10%, you achieved:")
            print(f"  a recovery acccuracy of: {100 * accuracy:.2f}%")
            print(f"  at a decoding rate of: {rate:.2f} letters/sec")
            print("-------------------------------------------------------")
        except Exception as e:
            print(f"Encoder/decoder crashed! It triggered the following exception:\n{e}")

    def test_noise_0_2(self):
        try:
            noise_prob = 0.2
            num_transmissions = 2000
            encoder = initialize_coder(noise_prob)
            accuracy, rate = measure_fidelity(encoder, num_transmissions, noise_prob,
                                              show_progress=False)
            print("\n-------------------------------------------------------")
            print(f"With a bit corruption probability of 20%, you achieved:")
            print(f"  a recovery acccuracy of: {100 * accuracy:.2f}%")
            print(f"  at a decoding rate of: {rate:.2f} letters/sec")
            print("-------------------------------------------------------")
        except Exception as e:
            print(f"Encoder/decoder crashed! It triggered the following exception:\n{e}")

