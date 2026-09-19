import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class CircleController(Node):
    def __init__(self):
        super().__init__('turtlebot3_circle_controller')
        self.velocity_publisher = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10,
        )
        self.timer = self.create_timer(0.1, self.publish_velocity)

        self.linear_speed = 0.15
        self.angular_speed = 0.5
        radius = self.linear_speed / self.angular_speed
        self.get_logger().info(
            f'Circle controller started; radius={radius:.2f} m'
        )

    def publish_velocity(self):
        velocity = TwistStamped()
        velocity.header.stamp = self.get_clock().now().to_msg()
        velocity.header.frame_id = 'base_link'
        velocity.twist.linear.x = self.linear_speed
        velocity.twist.angular.z = self.angular_speed
        self.velocity_publisher.publish(velocity)

    def stop(self):
        velocity = TwistStamped()
        velocity.header.stamp = self.get_clock().now().to_msg()
        velocity.header.frame_id = 'base_link'
        self.velocity_publisher.publish(velocity)


def main(args=None):
    rclpy.init(args=args)
    node = CircleController()

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if rclpy.ok():
            node.stop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
