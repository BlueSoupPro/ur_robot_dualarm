from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument("alice_ur_type", default_value="ur10"),
        DeclareLaunchArgument("bob_ur_type", default_value="ur10"),
        DeclareLaunchArgument("alice_robot_ip", default_value="192.168.56.101"),
        DeclareLaunchArgument("bob_robot_ip", default_value="192.168.10.100"),
        DeclareLaunchArgument("alice_use_mock_hardware", default_value="false"),
        DeclareLaunchArgument("bob_use_mock_hardware", default_value="false"),
        DeclareLaunchArgument("headless_mode", default_value="false"),
        DeclareLaunchArgument("alice_launch_dashboard_client", default_value="true"),
        DeclareLaunchArgument("bob_launch_dashboard_client", default_value="true"),
    ]

    common_arguments = {
        "alice_ur_type": LaunchConfiguration("alice_ur_type"),
        "bob_ur_type": LaunchConfiguration("bob_ur_type"),
        "alice_robot_ip": LaunchConfiguration("alice_robot_ip"),
        "bob_robot_ip": LaunchConfiguration("bob_robot_ip"),
        "alice_use_mock_hardware": LaunchConfiguration("alice_use_mock_hardware"),
        "bob_use_mock_hardware": LaunchConfiguration("bob_use_mock_hardware"),
        "headless_mode": LaunchConfiguration("headless_mode"),
    }

    start_robots = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("my_dual_robot_cell_control"),
                    "launch",
                    "start_robots.launch.py",
                ]
            )
        ),
        launch_arguments={
            **common_arguments,
            "alice_launch_dashboard_client": LaunchConfiguration(
                "alice_launch_dashboard_client"
            ),
            "bob_launch_dashboard_client": LaunchConfiguration(
                "bob_launch_dashboard_client"
            ),
            "launch_rviz": "false",
        }.items(),
    )

    move_group = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("my_dual_robot_cell_moveit_config"),
                    "launch",
                    "move_group.launch.py",
                ]
            )
        ),
        launch_arguments=common_arguments.items(),
    )

    moveit_rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("my_dual_robot_cell_moveit_config"),
                    "launch",
                    "moveit_rviz.launch.py",
                ]
            )
        ),
        launch_arguments=common_arguments.items(),
    )

    return LaunchDescription(declared_arguments + [start_robots, move_group, moveit_rviz])
