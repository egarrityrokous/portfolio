from abc import ABC, abstractmethod
from math import sqrt
from numpy.random import normal, multivariate_normal
from numpy import array, matmul, identity
from numpy.linalg import inv
from plane import CartesianPlane, AnimatedSprite, Slider, Message
import pygame as pg
from tracker import Tracker


class NaiveTracker(Tracker):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0)

    def update(self, observation):
        return observation


class KalmanTracker2D:
    def __init__(self, mu_0, sigma_x, sigma_z):
        self.F, self.H = identity(2), identity(2)
        self.sigma_x = sigma_x
        self.sigma_z = sigma_z
        self.mu_t = mu_0
        self.sigma_t = array([[0, 0], [0, 0]])

    def update(self, observation):
        z_1 = observation
        ftf = matmul(matmul(self.F, self.sigma_t), self.F.T)
        inverse_term = inv(matmul(matmul(self.H, ftf + self.sigma_x), self.H.T) + self.sigma_z)
        kalman_gain = matmul(matmul(ftf + self.sigma_x, self.H.T), inverse_term)
        f_times_mu_t = matmul(self.F, self.mu_t)
        self.mu_t = f_times_mu_t + matmul(kalman_gain, z_1 - matmul(self.H, f_times_mu_t))
        self.sigma_t = matmul(identity(len(z_1)) - matmul(kalman_gain, self.H),
                              matmul(matmul(self.F, self.sigma_t), self.F.T) + self.sigma_x)
        return tuple(self.mu_t)

    def reset_velocity_noise(self, velocity_noise):
        self.velocity_noise = velocity_noise
        self.sigma_x = velocity_noise

    def reset_sensor_noise(self, sensor_noise):
        self.sensor_noise = sensor_noise
        self.sigma_z = sensor_noise


class Squid(AnimatedSprite):

    SQUID_CELLS = []
    for i in range(1, 6):
        SQUID_CELLS += [f"images/squid{i}.png"] * 3
    for i in range(4, 1, -1):
        SQUID_CELLS += [f"images/squid{i}.png"] * 3

    def __init__(self, initial_x, initial_y):
        super().__init__((initial_x, initial_y), Squid.SQUID_CELLS, cell_scale=0.09)


class Target(AnimatedSprite):

    TARGET_CELLS = []
    for i in range(1, 9):
        TARGET_CELLS += [f"images/tracker{i}.png"] * 3
    for i in range(7, 1, -1):
        TARGET_CELLS += [f"images/tracker{i}.png"] * 3

    def __init__(self, initial_x, initial_y):
        super().__init__((initial_x, initial_y),
                         Target.TARGET_CELLS, cell_scale=0.09)


class TransitionModel:
    def __init__(self, F, sigma_x):
        self.F = array(F)
        self.sigma_x = array(sigma_x)

    def next_location(self, x_t, y_t):
        location = array([x_t, y_t]).T
        next_loc = multivariate_normal(matmul(self.F, location), self.sigma_x)
        return tuple(next_loc)


class Sensor:
    def __init__(self, H, sigma_z):
        self.H = array(H)
        self.sigma_z = array(sigma_z)

    def sense(self, x_t, y_t):
        location = array([x_t, y_t]).T
        sensed = multivariate_normal(matmul(self.H, location), self.sigma_z)
        return tuple(sensed)


class SquidGame:

    def __init__(self, tracker, initial_position):
        pg.init()
        if not pg.font:
            print("Warning, fonts disabled")
        if not pg.mixer:
            print("Warning, sound disabled")
        else:
            pg.mixer.init()
            pg.mixer.music.load('sounds/sonar.wav')
            pg.mixer.music.play(-1)
        pg.display.set_caption("Sonar")
        pg.mouse.set_visible(True)
        self.plane = CartesianPlane(x_max=30, y_max=10, screen_width=1200, screen_height=400)
        self.skittishness = Slider(20, 20, 100, "skittishness", initial_percentage=0.1)
        self.plane.add_widget(self.skittishness)
        self.sensor_noise = Slider(20, 80, 100, "sensor noise", initial_percentage=0.5)
        self.plane.add_widget(self.sensor_noise)
        self.position = initial_position
        self.squid = Squid(self.position[0], self.position[1])
        self.target = Target(self.position[0], self.position[1])
        self.message = Message(50, 370, "-.--", "black", 20)
        self.plane.add_widget(self.message)
        self.plane.add_sprite(self.squid)
        self.plane.add_sprite(self.target)
        self.tracker = tracker

    def read_sliders(self):
        new_sigma_x = array([[2 * self.skittishness.current_percentage(), 0],
                             [0, 2 * self.skittishness.current_percentage()]])
        new_sigma_z = array([[4 * self.sensor_noise.current_percentage(), 0],
                             [0, 4 * self.sensor_noise.current_percentage()]])
        return new_sigma_x, new_sigma_z

    def start(self):
        sigma_x, sigma_z = self.read_sliders()
        sensor = Sensor(identity(2), sigma_z)
        transition_model = TransitionModel(identity(2), sigma_x)
        clock = pg.time.Clock()
        going = True
        avg_distance_numerator, avg_distance_denominator = 0, 0
        while going:
            clock.tick(60)
            if self.squid.is_stationary():
                squid_x, squid_y = self.squid.current_position()
                target_x, target_y = self.target.current_position()
                distance = sqrt((squid_x - target_x)**2 + (squid_y - target_y)**2)
                avg_distance_numerator += distance
                avg_distance_denominator += 1
                avg_distance = f"{avg_distance_numerator / avg_distance_denominator:.2f}"
                self.message.reset_message(avg_distance)
                sigma_x, sigma_z = self.read_sliders()
                self.tracker.reset_sensor_noise(sigma_z)
                self.tracker.reset_velocity_noise(sigma_x)
                transition_model.sigma_x = sigma_x
                sensor.sigma_z = sigma_z
                delta_x, delta_y = transition_model.next_location(0, 0)
                valid_x, valid_y = self.plane.in_bounds(self.position[0] + delta_x,
                                                        self.position[1] + delta_y)
                if not valid_x:
                    delta_x = -delta_x
                if not valid_y:
                    delta_y = -delta_y
                self.squid.move(delta_x, delta_y)
                self.position = (self.position[0] + delta_x, self.position[1] + delta_y)
                observation = sensor.sense(self.position[0], self.position[1])
                estimated_x, estimated_y = self.tracker.update(observation)
                self.target.move(estimated_x - target_x, estimated_y - target_y)
            for event in pg.event.get():
                self.plane.notify(event)
                if event.type == pg.QUIT:
                    going = False
            self.plane.refresh()
        pg.quit()


def main():
    initial_position = (15, 5)
    tracker = KalmanTracker2D(mu_0=array(list(initial_position)).T,
                              sigma_x=None, sigma_z=None)
    #tracker = NaiveTracker()
    game = SquidGame(tracker, initial_position)
    game.start()


if __name__ == '__main__':
    main()
