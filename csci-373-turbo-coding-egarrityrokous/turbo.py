import argparse
import pygame as pg
import random
import time
from tqdm import tqdm
from plane import CartesianPlane, Message
from coder import initialize_coder, ALPHABETIC_ENCODINGS
from util import transmit, measure_fidelity


class Visualizer:
    """A friendly GUI for visualizing transmissions."""

    def __init__(self, coder, noise_prob):
        pg.init()
        if not pg.font:
            print("Warning, fonts disabled")
        if not pg.mixer:
            print("Warning, sound disabled")
        pg.display.set_caption("Turbo")
        pg.mouse.set_visible(True)
        self.coder = coder
        self.noise_prob = noise_prob
        self.plane = CartesianPlane(x_max=20, y_max=8, screen_width=800, screen_height=260)
        self.letters = []
        self.msg = "aquickbrownfoxjumpsoverthelazydog" * 3
        self.current_msg_ptr = 0
        self.accuracy_monitor = Message(10, 2, f"accuracy: --.-%", "yellow", 30)
        self.rate_monitor = Message(10, 1, f"decoding rate: --.-%", (255,200,42), 30)
        self.reset(self.msg[self.current_msg_ptr:self.current_msg_ptr+19])
        self.current_msg_ptr = (self.current_msg_ptr + 19) % 33

    def reset(self, msg):
        self.plane.clear()
        self.letters = []
        for i, letter in enumerate(msg):
            letter_obj = Message(1 + i, 7, letter, "white", 20)
            self.letters.append(letter_obj)
            self.plane.put(letter_obj)
        self.plane.put(self.accuracy_monitor)
        self.plane.put(self.rate_monitor)

    def blocking_move(self, letter, delta_x, delta_y, clock):
        letter.move(delta_x, delta_y)
        while not letter.is_stationary():
            clock.tick(60)
            self.plane.refresh()

    def start(self):
        delta_x, delta_y = 0, -1
        clock = pg.time.Clock()
        pg.event.get()
        going = True
        successes, attempts = 0, 0
        decoding_time = 0
        while going:
            for letter in self.letters:
                attempts += 1
                self.blocking_move(letter, delta_x, delta_y, clock)
                original_letter = letter.text
                encoding = self.coder.encode(letter.text)
                transmission = transmit(encoding, self.noise_prob)
                if encoding != transmission:
                    letter.reset_message("@")
                    letter.reset_color("orange")
                self.blocking_move(letter, delta_x, -2, clock)
                decoding_start = time.time()
                decoding = self.coder.decode(transmission)
                decoding_time += (time.time() - decoding_start)
                letter.reset_message(decoding)
                if decoding != original_letter:
                    letter.reset_color("red")
                else:
                    successes += 1
                    letter.reset_color("green")
                for event in pg.event.get():
                    self.plane.notify(event)
                    if event.type == pg.QUIT:
                        going = False
                if not going:
                    break
                accuracy = 100 * (successes/attempts)
                decoding_rate = attempts / decoding_time
                self.accuracy_monitor.reset_message(f"accuracy: {accuracy:.2f}%")
                self.rate_monitor.reset_message(f"decoding rate: {decoding_rate:.1f} letters/sec")
            self.reset(self.msg[self.current_msg_ptr:self.current_msg_ptr + 19])
            self.current_msg_ptr = (self.current_msg_ptr + 19) % 33
        pg.quit()


def main():
    parser = argparse.ArgumentParser(description='Play Wordle with your search-based agent.')
    parser.add_argument('-t', '--num_transmissions', required=False, type=int, default=0,
                        help='number of letters to transmit')
    parser.add_argument('-p', '--noise_prob', required=True, type=float,
                        help='the probability of bit corruption during transmission')
    args = parser.parse_args()
    coder = initialize_coder(args.noise_prob)
    if args.num_transmissions == 0:
        visualizer = Visualizer(coder, noise_prob=args.noise_prob)
        visualizer.start()
    else:
        accuracy, decoding_rate = measure_fidelity(coder, args.num_transmissions,
                                               args.noise_prob)
        print(f"Accuracy: {100*accuracy:.2f}%")
        print(f"Decoding rate: {decoding_rate:.2f} letters/sec")


if __name__ == '__main__':
    main()
