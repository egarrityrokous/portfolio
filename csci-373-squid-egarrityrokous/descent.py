from plane import CartesianPlane, AnimatedSprite, Message
import pygame as pg
from tqdm import tqdm
import argparse
from tracker import VelocityBasedTracker, SensorBasedTracker, KalmanTracker
from tracker import MotionModel, Sensor
from tracker import simulate_trajectory, track_trajectory

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class WhaleSprite(AnimatedSprite):
    def __init__(self, initial_x, initial_y):
        super().__init__((initial_x, initial_y),
                         ["images/whale{}.png".format(index) for index in range(1, 11)],
                         cell_scale=0.06)

class GhostWhale(AnimatedSprite):
    def __init__(self, initial_x, initial_y):
        super().__init__((initial_x, initial_y),
                         ["images/whaleghost{}.png".format(index) for index in range(1, 9)] + ["images/whale{}.png".format(index) for index in range(7, 1, -1)],
                         cell_scale=0.06)


class ErrorBar(AnimatedSprite):
    def __init__(self, initial_x, initial_y):
        super().__init__((initial_x, initial_y), ["images/error.png"], cell_scale=0.03)



def visualizer(positions, estimates, errors):
    if not pg.font:
        print("Warning, fonts disabled")
    if not pg.mixer:
        print("Warning, sound disabled")
    else:
        pg.mixer.init()
        pg.mixer.music.load('sounds/sonar.wav')
        pg.mixer.music.play(-1)
    pg.init()
    pg.display.set_caption("Descent")
    pg.mouse.set_visible(True)
    plane = CartesianPlane(x_max=5, y_max=20, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
    whale = WhaleSprite(1, 18-positions[0])
    tracker_sprites = dict()
    error_bars = dict()
    plane.add_sprite(whale)
    x_position = 2
    for tracker_name in estimates:
        tracker_sprites[tracker_name] = GhostWhale(x_position, 18-estimates[tracker_name][0])
        error_bars[tracker_name] = ErrorBar(x_position, 0)
        plane.add_sprite(tracker_sprites[tracker_name])
        plane.add_sprite(error_bars[tracker_name])
        whale_name = Message(x_position * SCREEN_WIDTH // 5, 20, tracker_name, "white", 15)
        plane.add_widget(whale_name)
        x_position += 1
    clock = pg.time.Clock()
    going = True
    time_step = 10
    while going:
        clock.tick(60)
        if whale.is_stationary() and time_step < len(positions):
            whale.move(0, positions[time_step-10] - positions[time_step])
            for tracker_name in error_bars:
                error_bars[tracker_name].move(0, sum(errors[tracker_name][time_step-10:time_step])/10)
                tracker_sprites[tracker_name].move(0, estimates[tracker_name][time_step-10] - estimates[tracker_name][time_step])
            time_step += 10
        for event in pg.event.get():
            plane.notify(event)
            if event.type == pg.QUIT:
                going = False
        plane.refresh()
    pg.quit()


def main(trackers, maximum_depth, motion_model, sensor):
    trajectory = simulate_trajectory(motion_model, starting_position=1.0, finish_line=maximum_depth)
    estimates, errors = track_trajectory(trajectory, sensor, trackers)
    visualizer(trajectory, estimates, errors)


def evaluate(trackers, maximum_depth, motion_model, sensor, num_descents=5):
    total_errors = {tracker: 0 for tracker in trackers}
    for _ in tqdm(range(num_descents)):
        for tracker in trackers:
            trackers[tracker].start_new_descent()
        trajectory = simulate_trajectory(motion_model, starting_position=1.0, finish_line=maximum_depth)
        estimates, errors = track_trajectory(trajectory, sensor, trackers)
        for tracker in trackers:
            total_errors[tracker] = total_errors[tracker] + sum(errors[tracker])
    average_error = {tracker: total_errors[tracker] / num_descents for tracker in trackers}
    for tracker in average_error:
        print(f'{tracker} error: {average_error[tracker]:.2f}')


def dispatch(args):
    possible_tracker_names = {"velocity", "sensor", "kalman"}
    tracker_names = args.trackers.split(',')
    for tracker_name in tracker_names:
        if tracker_name not in possible_tracker_names:
            raise ValueError(
                f"Unrecognized tracker: '{tracker_name}'.\nOnly the following are recognized: {possible_tracker_names}")
    starting_depth = 1
    avg_velocity = 0.1
    sigma_x = float(args.sigma_x)
    sigma_z = float(args.sigma_z)
    motion_model = MotionModel(avg_velocity, sigma_x)
    sensor = Sensor(sigma_z)
    trackers = dict()
    if 'kalman' in tracker_names:
        trackers['kalman'] = KalmanTracker(starting_depth, motion_model, sensor)
    if 'velocity' in tracker_names:
        trackers['velocity'] = VelocityBasedTracker(starting_depth, motion_model)
    if 'sensor' in tracker_names:
        trackers['sensor'] = SensorBasedTracker()
    if args.evaluate:
        evaluate(trackers, 18, motion_model, sensor, num_descents=1000)
    else:
        main(trackers, 18, motion_model, sensor)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tracks the descent of a whale in the ocean.')
    parser.add_argument('-x', '--velocity_noise', dest='sigma_x', required=False, default=0.1,
                        help='standard deviation of the transition model')
    parser.add_argument('-z', '--sensor_noise', dest='sigma_z', required=False, default=0.9,
                        help='standard deviation of the sensor')
    parser.add_argument('-e', '--evaluate', dest='evaluate', action='store_true', default=False,
                        help='evaluate the trackers, without visualizing them')
    parser.add_argument('-t', '--trackers', dest='trackers', default="velocity,sensor,kalman",
                        help='compare the specified trackers ("velocity", "sensor", "kalman")')
    dispatch(parser.parse_args())

