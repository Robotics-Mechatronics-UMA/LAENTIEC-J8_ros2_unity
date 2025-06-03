import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import math
import numpy as np


class IMUSubscriber(Node):
    def __init__(self):
        super().__init__('imu_subscriber')
        self.subscription = self.create_subscription(
            Imu,
            '/fixposition/imu',
            self.listener_callback,
            10
        )
        self.subscription  # Prevent unused variable warning


        # Variables de estado
        self.last_time = None
        self.position = np.zeros(3)  # [x, y, z] en metros
        self.velocity = np.zeros(3)  # [vx, vy, vz] en m/s

        # Parámetro para calcular aceleración en rpm
        self.wheel_radius = 0.28  # Radio de la rueda en metros (ajustar según el robot)


    def listener_callback(self, msg):
        # Obtener el tiempo actual
        current_time = self.get_clock().now().to_msg()
        current_time_sec = current_time.sec + current_time.nanosec * 1e-9

        if self.last_time is None:
            self.last_time = current_time_sec
            return

        # Calcular delta de tiempo (dt)
        dt = current_time_sec - self.last_time
        self.last_time = current_time_sec

        # Extraer datos de aceleración lineal
        accel = np.array([msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z])

        # Comprobar si la aceleración es prácticamente cero (robot detenido)
        accel_magnitude = np.linalg.norm(accel)
        if accel_magnitude < 1e-3:  # Tolerancia para ruido de aceleración
            self.velocity = np.zeros(3)
        else:
            # Calcular nueva velocidad (v = v0 + a * dt)
            self.velocity += accel * dt

        # Calcular nueva posición (x = x0 + v * dt) (Posición publicada por el nodo de Odometria)
        self.position += self.velocity * dt

        # Convertir velocidades y aceleraciones
        velocity_kmh = self.velocity * 3.6  # Velocidad en km/h
        velocity_kmh_magnitude = np.linalg.norm(velocity_kmh)  # Magnitud de la velocidad en km/h
        accel_rpm = (accel * 60) / (2 * math.pi * self.wheel_radius)  # Aceleración en rpm
        accel_rpm_magnitude = np.linalg.norm(accel_rpm)  # Magnitud de la aceleración en rpm

        # Obtener la orientación (cuaterniones) del mensaje
        orientation = msg.orientation
        roll, pitch, yaw = self.quaternion_to_euler(
            orientation.x, orientation.y, orientation.z, orientation.w
        )

        #Conversion a grados de la orientacion
        roll_deg = math.degrees(roll)
        pitch_deg = math.degrees(pitch)
        yaw_deg = math.degrees(yaw)


        # Mostrar resultados procesados
        self.get_logger().info("--- IMU Processed Data ---")
        #self.get_logger().info(f"Position (m): x={self.position[0]:.3f}, y={self.position[1]:.3f}, z={self.position[2]:.3f}")
        self.get_logger().info(f"Velocity (m/s): x={self.velocity[0]:.3f}, y={self.velocity[1]:.3f}, z={self.velocity[2]:.3f}")
        self.get_logger().info(f"Velocity (km/h): x={velocity_kmh[0]:.3f}, y={velocity_kmh[1]:.3f}, z={velocity_kmh[2]:.3f}, Magnitude={velocity_kmh_magnitude:.3f}")
        self.get_logger().info(f"Linear acceleration (m/s2): x={accel[0]:.3f}, y={accel[1] :.3f}, z={accel[2]:.3f}")
        self.get_logger().info(f"Acceleration (rpm): x={accel_rpm[0]:.3f}, y={accel_rpm[1]:.3f}, z={accel_rpm[2]:.3f}, Magnitude={accel_rpm_magnitude:.3f}")
        self.get_logger().info(f"Orientation (radians): roll={roll:.3f}, pitch={pitch:.3f}, yaw={yaw:.3f}")
        self.get_logger().info(f"Orientation (degrees): roll={roll_deg:.3f}, pitch={pitch_deg:.3f}, yaw={yaw_deg:.3f}")


    @staticmethod
    def quaternion_to_euler(x, y, z, w):
        
        #Convierte un cuaternión a ángulos de Euler (roll, pitch, yaw).
        
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t3, t4)

        return roll, pitch, yaw


def main(args=None):
    rclpy.init(args=args)
    imu_subscriber = IMUSubscriber()
    rclpy.spin(imu_subscriber)
    imu_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

