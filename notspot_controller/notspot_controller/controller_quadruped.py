#!/usr/bin/env python3
# Author: lnotspotl

import rclpy
import rclpy.logging
from rclpy.node import Node
from sensor_msgs.msg import Joy, Imu
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from .RobotController import RobotController
from .InverseKinematics import robot_IK


class RobotControllerNode(Node):
    def __init__(self):
        super().__init__("robot_controller")

        # Parámetros de configuración
        USE_IMU = True
        RATE = 60

        # Geometría del robot
        body = [0.1908, 0.080]
        legs = [0.0, 0.04, 0.100, 0.094333]

        # Inicialización de clases del robot
        self.notspot_robot = RobotController.Robot(body, legs, USE_IMU)
        self.inverse_kinematics = robot_IK.InverseKinematics(body, legs)

        # Publicador para trayectorias de las articulaciones
        self.joint_trajectory_publisher = self.create_publisher(JointTrajectory, "/joint_group_effort_controller/joint_trajectory", 10)

        # Subscripciones
        if USE_IMU:
            self.create_subscription(Imu, "notspot_imu/base_link_orientation", self.notspot_robot.imu_orientation, 10)
        self.create_subscription(Joy, "notspot_joy/joy_ramped", self.notspot_robot.joystick_command, 10)

        # Variables internas
        self.timer = self.create_timer(1/RATE, self.update_robot)

        self.get_logger().info("Robot Controller Node has been initialized.")
    def update_robot(self):
        """Ejecuta la lógica principal del robot."""
        try:
            # Obtener posiciones de las patas y actualizar el controlador

            leg_positions = self.notspot_robot.run()
            self.notspot_robot.change_controller()
            # Obtener la posición y orientación del cuerpo del robot
            dx = self.notspot_robot.state.body_local_position[0]
            dy = self.notspot_robot.state.body_local_position[1]
            dz = self.notspot_robot.state.body_local_position[2]
            roll = self.notspot_robot.state.body_local_orientation[0]
            pitch = self.notspot_robot.state.body_local_orientation[1]
            yaw = self.notspot_robot.state.body_local_orientation[2]
            # Calcular los ángulos de las articulaciones
            joint_angles = self.inverse_kinematics.inverse_kinematics(
                leg_positions, dx, dy, dz, roll, pitch, yaw
            )
            # Crear y publicar el mensaje de trayectoria de articulaciones
            joint_trajectory_msg = JointTrajectory()

            joint_trajectory_msg.joint_names = [
                "FR1_joint", "FR2_joint", "FR3_joint",  # Nombres de las articulaciones
                "FL1_joint", "FL2_joint", "FL3_joint",
                "RR1_joint", "RR2_joint", "RR3_joint",
                "RL1_joint", "RL2_joint", "RL3_joint"
            ]
            point = JointTrajectoryPoint()
            point.positions = joint_angles  # Usar posiciones calculadas


            joint_trajectory_msg.points.append(point)

            self.joint_trajectory_publisher.publish(joint_trajectory_msg)

        except Exception as e:
            self.get_logger().error(f"Error during robot update: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = RobotControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Robot Controller Node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
