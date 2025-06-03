#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ControlNode(Node):

    def __init__(self):
        super().__init__("control_node") #Mismo nombre que el ejecutable
        self.counter_ = 0
        self.get_logger().info("Control node iniciated")
        self.create_timer(0.5, self.timer_callback)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10) #Para atender la velocidad

    def timer_callback(self):
        self.counter_ += 1
        self.get_logger().info("Position " + str(self.counter_) + ":" + str(self.publisher_))
        msg = Twist()
        

        #Congifurar para mover el cubo
        msg.linear.x = 1.0 #Mover el cubo hacia delante
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg) #type:ignore

def main(args=None):
    rclpy.init(args=args)
    node = ControlNode() #Mismo nombre que la clase de nodo.
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()