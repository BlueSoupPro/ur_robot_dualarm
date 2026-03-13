from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_moveit_rviz_launch


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument("alice_ur_type", default_value="ur3e"),
        DeclareLaunchArgument("bob_ur_type", default_value="ur5e"),
        DeclareLaunchArgument("alice_robot_ip", default_value="192.168.57.101"),
        DeclareLaunchArgument("bob_robot_ip", default_value="192.168.57.100"),
        DeclareLaunchArgument("alice_use_mock_hardware", default_value="false"),
        DeclareLaunchArgument("bob_use_mock_hardware", default_value="false"),
        DeclareLaunchArgument("headless_mode", default_value="false"),
    ]

    moveit_config = (
        MoveItConfigsBuilder(
            "my_dual_robot_cell", package_name="my_dual_robot_cell_moveit_config"
        )
        .robot_description(
            mappings={
                "alice_ur_type": LaunchConfiguration("alice_ur_type"),
                "bob_ur_type": LaunchConfiguration("bob_ur_type"),
                "alice_robot_ip": LaunchConfiguration("alice_robot_ip"),
                "bob_robot_ip": LaunchConfiguration("bob_robot_ip"),
                "alice_use_mock_hardware": LaunchConfiguration("alice_use_mock_hardware"),
                "bob_use_mock_hardware": LaunchConfiguration("bob_use_mock_hardware"),
                "headless_mode": LaunchConfiguration("headless_mode"),
            }
        )
        .robot_description_semantic()
        .robot_description_kinematics()
        .trajectory_execution()
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True,
        )
        .joint_limits()
        .to_moveit_configs()
    )
    return LaunchDescription(declared_arguments + list(generate_moveit_rviz_launch(moveit_config).entities))
