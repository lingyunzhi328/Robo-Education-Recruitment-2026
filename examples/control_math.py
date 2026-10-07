"""Pure, testable point controller for the turtlesim teaching exercise."""
import math


def point_command(x, y, theta, goal_x=7.0, goal_y=7.0):
    distance = math.hypot(goal_x - x, goal_y - y)
    if distance < 0.15:
        return 0.0, 0.0
    desired = math.atan2(goal_y - y, goal_x - x)
    error = math.atan2(math.sin(desired - theta), math.cos(desired - theta))
    angular = max(-1.5, min(1.5, 2.0 * error))
    linear = min(1.0, 0.8 * distance) if abs(error) < 0.5 else 0.0
    return linear, angular
