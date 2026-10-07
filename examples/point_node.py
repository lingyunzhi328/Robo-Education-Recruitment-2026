"""Subscribe to turtlesim pose and send bounded point-control commands."""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from control_math import point_command


class PointNode(Node):
    def __init__(self):
        super().__init__("point_controller")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscription = self.create_subscription(Pose, "/turtle1/pose", self.update, 10)

    def update(self, pose):
        linear, angular = point_command(pose.x, pose.y, pose.theta)
        message = Twist()
        message.linear.x = linear
        message.angular.z = angular
        self.publisher.publish(message)


def main():
    rclpy.init()
    node = PointNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publisher.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
