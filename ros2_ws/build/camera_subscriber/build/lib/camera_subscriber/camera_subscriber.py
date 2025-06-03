import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        #Instancia de CvBridge, para convertir entre imágenes de ROS y matrices de imágenes en OpenCV.
        self.bridge = CvBridge() 
        self.get_logger().info("Camera Subscriber Node started, listening on /camera/image_raw")

    def listener_callback(self, msg):
        self.get_logger().info("Received image frame")
        # Convertir el mensaje ROS2 a un formato de OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        # Mostrar la imagen
        cv2.imshow("Camera Image", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = CameraSubscriber()
    rclpy.spin(camera_subscriber)
    camera_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
