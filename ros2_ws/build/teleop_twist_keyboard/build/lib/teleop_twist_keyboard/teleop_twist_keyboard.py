#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

class TeleopTwist(Node):
    def __init__(self):
        super().__init__('teleop_twist')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.twist = Twist()
        self.linear_speed = 0.0
        self.angular_speed = 0.0


    def publish_twist(self, linear, angular):
        self.twist.linear.x = linear
        self.twist.angular.z = angular
        self.pub.publish(self.twist)
    
    def handle_keyboard_input(self):
        settings = termios.tcgetattr(sys.stdin)
        print("Keyboard control: Use W/S to move forward/backward, A/D to turn. Press Ctrl+C to exit.")
        try:
            while True:
                key = get_key()
                if key == 'w':
                    self.publish_twist(5.0, 0.0)  # Avanzar
                elif key == 's':
                    self.publish_twist(-5.0, 0.0)  # Retroceder
                elif key == 'a':
                    self.publish_twist(0.0, 5.0)  # Girar izquierda
                elif key == 'd':
                    self.publish_twist(0.0, -5.0)  # Girar derecha
                elif key == ' ':
                    self.publish_twist(0.0, 0.0)  # Detener
                elif key == '\x03':  # Ctrl+C para salir
                    break
                else:
                    self.publish_twist(0.0, 0.0)  # Detener
        except Exception as e:
            print(e)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    
    
def main(args=None):
    rclpy.init(args=args)
    teleop = TeleopTwist()

    try:
            teleop.handle_keyboard_input()
    finally:
        teleop.destroy_node()
        rclpy.shutdown()

def get_key():
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__ == '__main__':
    main()
