import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
from launch_ros.actions import Node

def generate_launch_description():
    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="false",
    )

    use_slam = LaunchConfiguration("use_slam")

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_description'),
            'launch',
            'gazebo.launch.py',
        )
    )

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_controller'),
            'launch',
            'controller.launch.py',
        )
    )

    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('alanbot_controller'),
            'launch',
            'joystick_teleop.launch.py',
        )
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

    rviz_localization = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(
            get_package_share_directory('alanbot_localization'),
            "rviz",
            "global_localization.rviz"
        )],
        output='screen',
        parameters=[{"use_sim_time": True}],
        condition=UnlessCondition(use_slam)
    )

    rviz_slam = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(
            get_package_share_directory("alanbot_mapping"),
            "rviz",
            "slam.rviz"
        )],
        output="screen",
        parameters=[{"use_sim_time": True}],
        condition=IfCondition(use_slam)
    )

    return LaunchDescription([
        use_slam_arg,
        gazebo,
        controller,
        joystick,
        localization,
        slam,
        rviz_localization,
        rviz_slam
    ])
