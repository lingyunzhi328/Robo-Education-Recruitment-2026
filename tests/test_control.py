import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from control_math import point_command


class PointControlTests(unittest.TestCase):
    def test_stops_within_tolerance(self):
        self.assertEqual(point_command(7, 7, 0), (0.0, 0.0))

    def test_large_heading_error_rotates_first(self):
        v, w = point_command(1, 1, -math.pi / 2)
        self.assertEqual(v, 0)
        self.assertLessEqual(abs(w), 1.5)

    def test_angle_wrap_chooses_short_turn(self):
        v, w = point_command(0, 0, math.pi - 0.01, -1, -0.01)
        self.assertGreater(v, 0)
        self.assertGreater(w, 0)
        self.assertLess(w, 0.1)

    def test_simulated_unicycle_reaches_goal(self):
        x, y, theta = 5.544, 5.544, 0.0
        dt = 0.02
        for _ in range(1000):
            v, w = point_command(x, y, theta)
            x += dt * v * math.cos(theta)
            y += dt * v * math.sin(theta)
            theta += dt * w
        self.assertLess(math.hypot(x - 7, y - 7), 0.15)
        self.assertEqual(point_command(x, y, theta), (0, 0))


if __name__ == "__main__":
    unittest.main()
