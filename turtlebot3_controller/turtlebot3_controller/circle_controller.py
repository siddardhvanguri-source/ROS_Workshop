import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class CircleController(Node):
    def __init__(self):
        super().__init__('turtlebot3_circle_controller')
        self.velocity_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_velocity)

        self.linear_speed = 0.2
        self.angular_speed = 0.5
        self.get_logger().info('Circle controller started')

    def publish_velocity(self):
        velocity = Twist()
        velocity.linear.x = self.linear_speed
        velocity.angular.z = self.angular_speed
        self.velocity_publisher.publish(velocity)


def main(args=None):
    rclpy.init(args=args)
    node = CircleController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.velocity_publisher.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
