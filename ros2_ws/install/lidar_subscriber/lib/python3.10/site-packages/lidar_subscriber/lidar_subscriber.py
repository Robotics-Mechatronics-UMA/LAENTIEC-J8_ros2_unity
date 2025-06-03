import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LiDARSubscriber(Node):

    def __init__(self):
        super().__init__('lidar_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/lidar_scan',
            self.lidar_callback,
            10)  
        self.subscription  # evita el warning de variable sin usar

    def lidar_callback(self, msg):
        self.get_logger().info(f'Received LiDAR scan: {msg.ranges[:10]}')
def main(args=None):
    rclpy.init(args=args)
    node = LiDARSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

