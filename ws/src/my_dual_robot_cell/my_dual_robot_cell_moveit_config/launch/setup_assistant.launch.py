from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_setup_assistant_launch


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder(
            "my_dual_robot_cell", package_name="my_dual_robot_cell_moveit_config"
        )
        .robot_description(
            mappings={
                "alice_ur_type": "ur3e",
                "bob_ur_type": "ur5e",
                "alice_robot_ip": "192.168.57.101",
                "bob_robot_ip": "192.168.57.100",
                "alice_use_mock_hardware": "true",
                "bob_use_mock_hardware": "true",
                "headless_mode": "true",
            }
        )
        .robot_description_semantic()
        .robot_description_kinematics()
        .trajectory_execution()
        .joint_limits()
        .to_moveit_configs()
    )
    return generate_setup_assistant_launch(moveit_config)
