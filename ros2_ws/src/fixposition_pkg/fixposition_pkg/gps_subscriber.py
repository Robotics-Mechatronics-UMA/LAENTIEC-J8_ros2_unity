import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

class GPSSubscriber(Node):
    def __init__(self):
        super().__init__('gps_subscriber')
        self.subscription = self.create_subscription(
            NavSatFix,
            '/fixposition/navsatfix',
            self.listener_callback,
            10
        )
        self.subscription  # para evitar advertencias sin usar

    def listener_callback(self, msg):
        self.get_logger().info(
            f'Recibido GPS -> Latitud: {msg.latitude}, Longitud: {msg.longitude}, Altitud: {msg.altitude}'
        )

def main(args=None):
    rclpy.init(args=args)
    gps_subscriber = GPSSubscriber()

    try:
        rclpy.spin(gps_subscriber)
    except KeyboardInterrupt:
        pass

    gps_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
