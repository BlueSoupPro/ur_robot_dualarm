# Run Guide

This document lists the commands needed to bring up the dual-arm URSim setup, the Jazzy workspace container, and the ROS 2 / MoveIt stack in this repository.

## Repository Root

All commands below assume this repository root:

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm
```

## 1. Start Two URSim Containers

Go to the simulator directory:

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm/ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator
```

Start both simulated robots:

```bash
docker compose up -d
docker compose ps
```

Open the web UIs:

- Alice: `http://localhost:6081`
- Bob: `http://localhost:6082`

Useful commands:

```bash
docker compose logs -f
docker compose down
```

## 2. Start the Jazzy Development Container

Go back to the repository root:

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm
```

Allow the container to open GUI applications on the host:

```bash
xhost +local:root
```

Build and enter the Jazzy container:

```bash
cd docker
docker compose build
docker compose run --rm dualbot
```

## 3. Build the Workspace

Inside the container:

```bash
cd /ws
rosdep update
rosdep install --ignore-src --from-paths src -y
colcon build --packages-up-to my_dual_robot_cell_moveit_config
source install/setup.bash
```

## 4. Bring Up the Full Dual-Arm Stack

Inside the container:

```bash
cd /ws
source install/setup.bash
ros2 launch my_dual_robot_cell_moveit_config bringup.launch.py
```

This one command starts:

- dual-arm `ur_robot_driver`
- `move_group`
- one MoveIt RViz instance

## 5. Start the External Control Programs in URSim

In the two URSim web UIs:

- on Alice, run `external_control_alice.urp`
- on Bob, run `external_control_bob.urp`

The ROS drivers will only be fully ready after those programs are running.

## 6. Useful Checks

Inside the container:

```bash
cd /ws
source install/setup.bash
ros2 node list
ros2 control list_controllers
ros2 topic list | grep alice
ros2 topic list | grep bob
```

## 7. Mock-Hardware Mode

If you want to test without URSim:

```bash
cd /ws
source install/setup.bash
ros2 launch my_dual_robot_cell_moveit_config bringup.launch.py \
  alice_use_mock_hardware:=true \
  bob_use_mock_hardware:=true
```

## 8. GPU Container Variant

If you want the GPU-enabled container:

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm/docker/docker_gpu
docker compose build
docker compose run --rm pickbot
```

## 9. Stop Everything

Stop the ROS stack by leaving the container shell or pressing `Ctrl+C` in the launch terminal.

Stop URSim:

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm/ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator
docker compose down
```
