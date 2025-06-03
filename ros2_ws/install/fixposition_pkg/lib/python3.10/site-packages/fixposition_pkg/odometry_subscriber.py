import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdometrySubscriber(Node):

    def __init__(self):
        super().__init__('odometry_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/fixposition/odometry',
            self.odometry_callback,
            10)  # Frecuencia de suscripción en Hz
        self.subscription  # Prevent unused variable warning

    def odometry_callback(self, msg):
        # Procesar los datos del mensaje
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        #linear_velocity = msg.twist.twist.linear
        #angular_velocity = msg.twist.twist.angular

        self.get_logger().info(f"Posición: x={position.x}, y={position.y}, z={position.z}")
        self.get_logger().info(f"Orientación: x={orientation.x}, y={orientation.y}, z={orientation.z}, w={orientation.w}")
        #self.get_logger().info(f"Velocidad Lineal: x={linear_velocity.x}, y={linear_velocity.y}, z={linear_velocity.z}")
        #self.get_logger().info(f"Velocidad Angular: x={angular_velocity.x}, y={angular_velocity.y}, z={angular_velocity.z}")

def main(args=None):
    rclpy.init(args=args)
    node = OdometrySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
