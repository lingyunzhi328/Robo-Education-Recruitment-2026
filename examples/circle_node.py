"""ROS 2 Jazzy: publish a circle command for eight seconds, then stop."""
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CircleNode(Node):
    def __init__(self):
        super().__init__("circle_controller")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.started = time.monotonic()
        self.timer = self.create_timer(0.1, self.tick)

    def tick(self):
        message = Twist()
        if time.monotonic() - self.started < 8.0:
            message.linear.x = 1.0
            message.angular.z = 1.0
        self.publisher.publish(message)


def main():
    rclpy.init()
    node = CircleNode()
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
