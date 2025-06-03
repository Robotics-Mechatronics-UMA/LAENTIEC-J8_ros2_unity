import sys
import threading
import geometry_msgs.msg
import rclpy
from rclpy.node import Node
from inputs import get_gamepad, devices

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')

        # Configuración del teclado
        if sys.platform != 'win32':
            self.settings = termios.tcgetattr(sys.stdin)

        # Modo de operación: Verifica si el gamepad está conectado
        self.use_gamepad = self.check_for_gamepad()

        # Mensaje de control
        self.msg = """
        This node takes keypresses from the keyboard and publishes them
        as Twist/TwistStamped messages. It works best with a US keyboard layout.
        ---------------------------
        Moving around:
        u    i    o
        j    k    l
        m    ,    .

        For Holonomic mode (strafing), hold down the shift key:
        ---------------------------
        U    I    O
        J    K    L
        M    <    >

        t : up (+z)
        b : down (-z)

        anything else : stop

        q/z : increase/decrease max speeds by 10%
        w/x : increase/decrease only linear speed by 10%
        e/c : increase/decrease only angular speed by 10%

        Gamepad (if connected):
        - Right joystick for angular velocity (turn)
        - Left joystick for linear velocity (forward/backward)
        - RT/ LT for speed control
        ---------------------------

        CTRL-C to quit
        """

        # Diccionarios de control
        self.moveBindings = {
            'i': (1, 0, 0, 0),
            'o': (1, 0, 0, -1),
            'j': (0, 0, 0, 1),
            'l': (0, 0, 0, -1),
            'u': (1, 0, 0, 1),
            ',': (-1, 0, 0, 0),
            '.': (-1, 0, 0, 1),
            'm': (-1, 0, 0, -1),
            'O': (1, -1, 0, 0),
            'I': (1, 0, 0, 0),
            'J': (0, 1, 0, 0),
            'L': (0, -1, 0, 0),
            'U': (1, 1, 0, 0),
            '<': (-1, 0, 0, 0),
            '>': (-1, -1, 0, 0),
            'M': (-1, 1, 0, 0),
            't': (0, 0, 1, 0),
            'b': (0, 0, -1, 0),
        }

        self.speedBindings = {
            'q': (1.1, 1.1),
            'z': (.9, .9),
            'w': (1.1, 1),
            'x': (.9, 1),
            'e': (1, 1.1),
            'c': (1, .9),
        }

    def check_for_gamepad(self):
        """Verifica si hay un gamepad (control XBOX) conectado."""
        if devices.gamepads:
            self.get_logger().info("Gamepad detected, using gamepad control.")
            return True
        else:
            self.get_logger().warn("No gamepad found, switching to keyboard control.")
            return False

    def getKey(self, settings):
        if sys.platform == 'win32':
            key = msvcrt.getwch()
        else:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def saveTerminalSettings(self):
        if sys.platform == 'win32':
            return None
        return termios.tcgetattr(sys.stdin)

    def restoreTerminalSettings(self, old_settings):
        if sys.platform == 'win32':
            return
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def vels(self, speed, turn):
        return 'currently:\tspeed %s\tturn %s ' % (speed, turn)

    def get_gamepad_input(self):
        """Capture and map gamepad input."""
        x = 0.0
        z = 0.0
        speed_multiplier = 0.0
        rt_value = 0
        lt_value = 0

        events = get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                if event.code == "ABS_RX":  # Joystick derecho - eje horizontal
                    z = self.map_range(event.state, -32768, 32767, -1.0, 1.0)
                elif event.code == "ABS_RY":  # Joystick izquierdo - eje vertical
                    x = self.map_range(event.state, -32768, 32767, -1.0, 1.0)
                elif event.code == "ABS_Z":  # Botón RT
                    rt_value = event.state
                elif event.code == "ABS_RZ":  # Botón LT
                    lt_value = event.state

        if rt_value > 0:
            speed_multiplier = rt_value / 255.0
        elif lt_value > 0:
            speed_multiplier = -lt_value / 255.0

        return x, z, speed_multiplier

    def map_range(self, value, left_min, left_max, right_min, right_max):
        left_span = left_max - left_min
        right_span = right_max - right_min
        value_scaled = float(value - left_min) / float(left_span)
        return right_min + (value_scaled * right_span)


def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()

    settings = node.saveTerminalSettings()

    stamped = node.declare_parameter('stamped', False).value
    frame_id = node.declare_parameter('frame_id', '').value

    if stamped:
        TwistMsg = geometry_msgs.msg.TwistStamped
    else:
        TwistMsg = geometry_msgs.msg.Twist

    pub = node.create_publisher(TwistMsg, 'cmd_vel', 10)

    spinner = threading.Thread(target=rclpy.spin, args=(node,))
    spinner.start()

    speed = 0.5
    turn = 1.0
    x = 0.0
    y = 0.0
    z = 0.0
    th = 0.0
    status = 0.0

    twist_msg = TwistMsg()
    if stamped:
        twist = twist_msg.twist
        twist_msg.header.stamp = node.get_clock().now().to_msg()
        twist_msg.header.frame_id = frame_id
    else:
        twist = twist_msg

    try:
        print(node.msg)
        print(node.vels(speed, turn))
        while True:
            if node.use_gamepad:
                x, th, speed_multiplier = node.get_gamepad_input()
                twist.linear.x = x * speed * speed_multiplier
                twist.angular.z = th * turn * speed_multiplier
            else:
                key = node.getKey(settings)
                if key in node.moveBindings.keys():
                    x = node.moveBindings[key][0]
                    y = node.moveBindings[key][1]
                    z = node.moveBindings[key][2]
                    th = node.moveBindings[key][3]
                elif key in node.speedBindings.keys():
                    speed = speed * node.speedBindings[key][0]
                    turn = turn * node.speedBindings[key][1]
                    print(node.vels(speed, turn))
                    if status == 14:
                        print(node.msg)
                    status = (status + 1) % 15
                else:
                    x = 0.0
                    y = 0.0
                    z = 0.0
                    th = 0.0
                    if key == '\x03':
                        break

                twist.linear.x = x * speed
                twist.angular.z = th * turn

            pub.publish(twist_msg)

    except Exception as e:
        print(e)

    finally:
        twist.linear.x = 0.0


if __name__ == '__main__':
    main()
