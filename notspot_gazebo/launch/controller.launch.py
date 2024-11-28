import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, AppendEnvironmentVariable, ExecuteProcess,RegisterEventHandler, ExecuteProcess, TimerAction, LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from ament_index_python.packages import get_package_prefix
from launch.event_handlers import OnProcessExit
def generate_launch_description():

    controller = Node(
        name='robot_controller',
        executable='controller_quadruped',
        package='notspot_controller',
        output='screen',
        emulate_tty='true'
    )
    ramped_controller = Node(
        name='notspot_joystick',
        executable='ramped_joystick',
        package='notspot_joystick',
        output='screen',
        emulate_tty='true'
    )



    return LaunchDescription([

        controller,
        ramped_controller
    ])