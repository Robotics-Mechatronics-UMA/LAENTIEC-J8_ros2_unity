#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class PoseSubscriber(Node):

    def __init__(self):
        super().__init__('pose_node')
        
        # Crear el suscriptor para el tópico 'robot_pose'
        self.subscription = self.create_subscription(
            PoseStamped,
            'robot_pose',
            self.pose_callback,
            10)
        
        self.get_logger().info("Pose Subscriber Node has started and is listening to /robot_pose topic")

    def pose_callback(self, msg):
        # Imprimir la posición y orientación recibida en el terminal
        self.get_logger().info(f"Received Pose: Position(x: {msg.pose.position.x}, y: {msg.pose.position.y}, z: {msg.pose.position.z})")
        self.get_logger().info(f"Orientation(x: {msg.pose.orientation.x}, y: {msg.pose.orientation.y}, z: {msg.pose.orientation.z}, w: {msg.pose.orientation.w})")

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
