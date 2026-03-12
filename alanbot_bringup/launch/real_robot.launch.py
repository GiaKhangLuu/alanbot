import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_slam_arg = DeclareLaunchArgument(
        'use_slam',
        default_value='false',
    )

    use_slam = LaunchConfiguration('use_slam')

    hardware_interface = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_firmware'),
            'launch',
            'hardware_interface.launch.py'
        )
    )

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_controller'),
            'launch',
            'controller.launch.py'
        )
    )

    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_controller'),
            'launch',
            'joystick_teleop.launch.py'
        )
    )

    laser_driver = Node(
        package="rplidar_ros",
        executable="rplidar_node",
        name="rplidar_node",
        parameters=[os.path.join(
            get_package_share_directory('alanbot_bringup'),
            'config',
            'rplidar_a1.yaml'
        )],
        output="screen",
    )

    localization = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_localization'),
            "launch",
            "global_localization.launch.py"
        ),
        condition=UnlessCondition(use_slam)
    )

    slam = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_mapping'),
            "launch",
            "slam.launch.py"
        ),
        condition=IfCondition(use_slam)
    )

    return LaunchDescription([
        use_slam_arg,
        hardware_interface,
        controller,
        joystick,
        laser_driver,
        localization,
        slam,
    ])
