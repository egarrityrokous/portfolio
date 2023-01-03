import unittest
from tracker import MotionModel, Sensor
from tracker import simulate_trajectory, track_trajectory
from tracker import SensorBasedTracker, VelocityBasedTracker, KalmanTracker


class ReproducibleMotionModel:

    def __init__(self, velocity_mean):
        self.velocity_mean = velocity_mean
        self.velocity_noise = 1.0
        self.noises = [-0.38, 0.07, -0.79, -0.05, -2.12, 0.73, -0.82, 0.81, -0.21, -0.68,
                       1.50, 0.15, 0.78, 0.10, -0.03, -0.83, -0.78, 0.65, -0.13, -0.17]
        self.current_noise = 0

    def move(self, current_position):
        distance = current_position + self.velocity_mean + self.noises[self.current_noise]
        self.current_noise = (self.current_noise + 1) % len(self.noises)
        return distance

    def get_average_velocity(self):
        return self.velocity_mean

    def get_velocity_noise(self):
        return self.velocity_noise


class ReproducibleSensor:

    def __init__(self):
        self.noises = [-0.82, 0.81, -0.21, -0.68, 1.50, 0.15, 0.78, 0.10, -0.03, -0.83,
                       -0.78, 0.65, -0.13, -0.17, -0.38, 0.07, -0.79, -0.05, -2.12, 0.73]
        self.current_noise = 0

    def sense(self, true_position):
        noise = self.noises[self.current_noise]
        self.current_noise = (self.current_noise + 1) % len(self.noises)
        return true_position + noise

    def get_sensor_noise(self):
        return 1.0



class TestOne(unittest.TestCase):

    def test_simulate_trajectory(self):
        motion_model = ReproducibleMotionModel(velocity_mean=1.0)
        simulated = simulate_trajectory(motion_model, starting_position=0, finish_line=20)
        expected = [0, 0.62, 1.69, 1.90, 2.85, 1.73, 3.46, 3.64, 5.45, 6.24, 6.56,
                    9.06, 10.21, 11.99, 13.09, 14.06, 14.23, 14.45, 16.1, 16.97, 17.8,
                    18.42, 19.49, 19.70, 20.65]
        self.assertEqual(len(simulated), len(expected))
        for i in range(len(simulated)):
            self.assertAlmostEqual(simulated[i], expected[i])

    def test_simulate_trajectory2(self):
        motion_model = ReproducibleMotionModel(velocity_mean=1.0)
        simulated = simulate_trajectory(motion_model, starting_position=25, finish_line=30)
        expected = [25, 25.62, 26.69, 26.90, 27.85, 26.73, 28.46, 28.64, 30.45]
        self.assertEqual(len(simulated), len(expected))
        for i in range(len(simulated)):
            self.assertAlmostEqual(simulated[i], expected[i])

class TestTwo(unittest.TestCase):

    def test_track_trajectory(self):
        sensor = ReproducibleSensor()
        trajectory = [5, 3.62, 2.69, 0.9]
        trackers = {'sensor': SensorBasedTracker()}
        tracked, errors = track_trajectory(trajectory, sensor, trackers)
        expected = {'sensor': [5, 2.80, 3.5, 0.69]}
        self.assertEqual(len(tracked['sensor']), len(expected['sensor']))
        for i in range(len(tracked['sensor'])):
            self.assertAlmostEqual(tracked['sensor'][i], expected['sensor'][i])
        expected = {'sensor': [0, 0.82, 0.81, 0.21]}
        self.assertEqual(len(errors['sensor']), len(expected['sensor']))
        for i in range(len(errors['sensor'])):
            self.assertAlmostEqual(errors['sensor'][i], expected['sensor'][i])

class TestThree(unittest.TestCase):

    def test_velocity_based_tracker(self):
        sensor = ReproducibleSensor()
        motion_model = ReproducibleMotionModel(velocity_mean=3.0)
        tracker = VelocityBasedTracker(start_position=2.0, motion_model=motion_model)
        trajectory = [2, 5.12, 8.02, 10.68]
        trackers = {'velocity': tracker}
        tracked, errors = track_trajectory(trajectory, sensor, trackers)
        expected = {'velocity': [2, 5, 8, 11]}
        self.assertEqual(len(tracked['velocity']), len(expected['velocity']))
        for i in range(len(tracked['velocity'])):
            self.assertAlmostEqual(tracked['velocity'][i], expected['velocity'][i])
        expected = {'velocity': [0, 0.12, 0.02, 0.32]}
        self.assertEqual(len(errors['velocity']), len(expected['velocity']))
        for i in range(len(errors['velocity'])):
            self.assertAlmostEqual(errors['velocity'][i], expected['velocity'][i])

    def test_velocity_based_tracker_twice_over(self):
        motion_model = ReproducibleMotionModel(velocity_mean=3.0)
        tracker = VelocityBasedTracker(start_position=2.0, motion_model=motion_model)
        trajectory = [2, 5.12, 8.02, 10.68]
        trackers = {'velocity': tracker}
        track_trajectory(trajectory, ReproducibleSensor(), trackers)
        tracked, errors = track_trajectory(trajectory, ReproducibleSensor(), trackers)
        expected = {'velocity': [2, 5, 8, 11]}
        self.assertEqual(len(tracked['velocity']), len(expected['velocity']))
        for i in range(len(tracked['velocity'])):
            self.assertAlmostEqual(tracked['velocity'][i], expected['velocity'][i])
        expected = {'velocity': [0, 0.12, 0.02, 0.32]}
        self.assertEqual(len(errors['velocity']), len(expected['velocity']))
        for i in range(len(errors['velocity'])):
            self.assertAlmostEqual(errors['velocity'][i], expected['velocity'][i])


class TestFour(unittest.TestCase):

    def test_kalman_tracker(self):
        sensor = ReproducibleSensor()
        motion_model = ReproducibleMotionModel(velocity_mean=3.0)
        tracker = KalmanTracker(start_position=2.0, motion_model=motion_model, sensor=sensor)
        trajectory = [2, 5.12, 8.02, 10.68]
        trackers = {'kalman': tracker}
        tracked, errors = track_trajectory(trajectory, sensor, trackers)
        expected = {'kalman': [2, 4.65, 8.358, 10.811538461538461]}
        self.assertEqual(len(tracked['kalman']), len(expected['kalman']))
        for i in range(len(tracked['kalman'])):
            self.assertAlmostEqual(tracked['kalman'][i], expected['kalman'][i])
        expected = {'kalman': [0, 0.46999999999999975, 0.33800000000000097, 0.1315384615384616]}
        self.assertEqual(len(errors['kalman']), len(expected['kalman']))
        for i in range(len(errors['kalman'])):
            self.assertAlmostEqual(errors['kalman'][i], expected['kalman'][i])

    def test_kalman_tracker_twiceover(self):
        motion_model = ReproducibleMotionModel(velocity_mean=3.0)
        tracker = KalmanTracker(start_position=2.0, motion_model=motion_model, sensor=ReproducibleSensor())
        trajectory = [2, 5.12, 8.02, 10.68]
        trackers = {'kalman': tracker}
        track_trajectory(trajectory, ReproducibleSensor(), trackers)
        tracked, errors = track_trajectory(trajectory, ReproducibleSensor(), trackers)
        expected = {'kalman': [2, 4.65, 8.358, 10.811538461538461]}
        self.assertEqual(len(tracked['kalman']), len(expected['kalman']))
        for i in range(len(tracked['kalman'])):
            self.assertAlmostEqual(tracked['kalman'][i], expected['kalman'][i])
        expected = {'kalman': [0, 0.46999999999999975, 0.33800000000000097, 0.1315384615384616]}
        self.assertEqual(len(errors['kalman']), len(expected['kalman']))
        for i in range(len(errors['kalman'])):
            self.assertAlmostEqual(errors['kalman'][i], expected['kalman'][i])



if __name__ == "__main__":
    unittest.main()   