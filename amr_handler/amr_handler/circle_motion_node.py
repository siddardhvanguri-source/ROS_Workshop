import rclpy
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class CircleMotionNode(Node):
    def __init__(self):
        super().__init__('circle_motion_node')
        self.declare_parameter('linear_speed', 0.2)
        self.declare_parameter('angular_speed', 0.5)
        self.declare_parameter('duration', 0.0)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        self.duration = self.get_parameter('duration').value
        self.started_at = self.get_clock().now()

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_circle_command)

        radius = self.linear_speed / self.angular_speed
        self.get_logger().info(
            f'Moving in a circle: radius={radius:.3f} m, '
            f'linear={self.linear_speed:.3f} m/s, '
            f'angular={self.angular_speed:.3f} rad/s'
        )

    def publish_circle_command(self):
        elapsed = (self.get_clock().now() - self.started_at).nanoseconds / 1e9
        if self.duration > 0.0 and elapsed >= self.duration:
            self.stop_robot()
            self.get_logger().info('Circle motion complete')
            rclpy.shutdown()
            return

        message = Twist()
        message.linear.x = self.linear_speed
        message.angular.z = self.angular_speed
        self.publisher.publish(message)

    def stop_robot(self):
        self.publisher.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    node = CircleMotionNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if rclpy.ok():
            node.stop_robot()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
