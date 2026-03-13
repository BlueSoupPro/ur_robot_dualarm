# UR Dual-Arm ROS 2 Workspace

This repository contains a ROS 2 Jazzy workspace for a dual-robot Universal Robots setup based on the official UR ROS 2 tutorials. It includes:

- a dual-arm workcell description
- dual-arm `ur_robot_driver` bringup
- a dual-arm URSim setup with two simulators
- a MoveIt configuration package for the dual-arm scene
- Docker environments for CPU and GPU workflows

For the command-only runbook, see [README_RUN.md](./README_RUN.md).

## Repository Layout

- `docker/`
  CPU container for the Jazzy workspace
- `docker/docker_gpu/`
  GPU-enabled container variant
- `ws/`
  ROS 2 workspace
- `ws/src/my_dual_robot_cell/my_dual_robot_cell_description/`
  dual-arm scene description
- `ws/src/my_dual_robot_cell/my_dual_robot_cell_control/`
  dual-arm driver, controllers, URSim setup
- `ws/src/my_dual_robot_cell/my_dual_robot_cell_moveit_config/`
  dual-arm MoveIt package

## What the Project Starts

The main one-command bringup is:

```bash
ros2 launch my_dual_robot_cell_moveit_config bringup.launch.py
```

That launch starts:

- the dual-arm UR drivers
- controller manager and joint controllers
- `move_group`
- one MoveIt RViz session

The dual-arm scene currently contains:

- `world`
- an internal `cell_origin` anchor link
- `alice_robot_mount`
- `bob_robot_mount`
- the two robot arms

The table, wall, and monitor have been removed from the scene so planning is done only against robot self-collision and dual-arm collision.

## How to Use the Project

### 1. Start URSim

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm/ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator
docker compose up -d
```

Web access:

- Alice: `http://localhost:6081`
- Bob: `http://localhost:6082`

### 2. Start the Jazzy Container

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm
xhost +local:root
cd docker
docker compose build
docker compose run --rm dualbot
```

### 3. Build the Workspace

Inside the container:

```bash
cd /ws
rosdep update
rosdep install --ignore-src --from-paths src -y
colcon build --packages-up-to my_dual_robot_cell_moveit_config
source install/setup.bash
```

### 4. Launch the Full Stack

Inside the container:

```bash
ros2 launch my_dual_robot_cell_moveit_config bringup.launch.py
```

Then in the URSim web UIs run:

- `external_control_alice.urp`
- `external_control_bob.urp`

## Hybrid Setup: One Simulated UR10 (`soup`) and One Real UR10

This repository can also run in a mixed setup:

- `alice` = simulated UR10 (`soup`)
- `bob` = real UR10

Recommended addressing:

- Pickbot PC host: `192.168.10.103`
- real UR10 (`bob`): `192.168.10.100`
- simulated UR10 (`soup` / `alice`): `192.168.56.101`
- Docker bridge gateway seen by `soup`: `192.168.56.1`

The dual-arm control xacro already uses separate ports for the two arms:

- `alice` script sender port: `50007`
- `bob` script sender port: `50002`

So this mixed layout matches your requirement that the real robot uses port `50002`.

### Start the simulated UR10 (`soup`)

Use the dedicated compose file:

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm/ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator
docker compose -f docker-compose.soup.yaml up -d
```

Web access:

- Soup URSim: `http://localhost:6083`

### Launch the mixed real + sim ROS stack

Inside the Jazzy container:

```bash
cd /ws
source install/setup.bash
ros2 launch my_dual_robot_cell_moveit_config bringup_soup_real.launch.py
```

This launch defaults to:

- `alice_ur_type:=ur10`
- `alice_robot_ip:=192.168.56.101`
- `bob_ur_type:=ur10`
- `bob_robot_ip:=192.168.10.100`

### External Control targets

Set the External Control targets like this:

- simulated UR10 (`soup` / `alice`): `192.168.56.1:50007`
- real UR10 (`bob`): `192.168.10.103:50002`

For the real robot, the host shown on the teach pendant can be the PC name `Pickbot PC`, but IP is more reliable. I recommend using `192.168.10.103:50002`.

### Files involved in this hybrid setup

- simulator compose:
  `ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator/docker-compose.soup.yaml`
- simulator persistent storage:
  `ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator/persistent_storage_soup/`
- dedicated bringup launch:
  `ws/src/my_dual_robot_cell/my_dual_robot_cell_moveit_config/launch/bringup_soup_real.launch.py`

## Changing the Simulated Robot Type in URSim

There are two separate places to think about when changing robot type:

1. the URSim container model
2. the ROS 2 robot description / driver type

They must be kept consistent.

### Where to Change the URSim Model

Edit:

`ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator/docker-compose.yml`

The current simulator service definitions use:

```yaml
environment:
  ROBOT_MODEL: "UR3"
```

and

```yaml
environment:
  ROBOT_MODEL: "UR5"
```

Change those values to the model you want the simulator to run.

### Where to Change the ROS Side

You can change robot type at launch time without editing source code:

```bash
ros2 launch my_dual_robot_cell_moveit_config bringup.launch.py \
  alice_ur_type:=ur10 \
  bob_ur_type:=ur10
```

The same arguments are passed through to:

- `my_dual_robot_cell_control/start_robots.launch.py`
- `my_dual_robot_cell_moveit_config/move_group.launch.py`
- `my_dual_robot_cell_moveit_config/moveit_rviz.launch.py`

So one launch command keeps the driver and MoveIt description aligned.

If you want to change the defaults permanently, edit:

- `ws/src/my_dual_robot_cell/my_dual_robot_cell_moveit_config/launch/bringup.launch.py`
- `ws/src/my_dual_robot_cell/my_dual_robot_cell_control/launch/start_robots.launch.py`

## Example: Simulate Two UR10 Robots

### 1. Change the URSim compose file

In:

`ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator/docker-compose.yml`

set both services to:

```yaml
environment:
  ROBOT_MODEL: "UR10"
```

### 2. Restart URSim

```bash
cd /home/hanchong/BlueSoupPro/ur_robot_dualarm/ws/src/my_dual_robot_cell/my_dual_robot_cell_control/dual-arm-simulator
docker compose down
docker compose up -d
```

### 3. Launch ROS for dual UR10

Inside the Jazzy container:

```bash
cd /ws
source install/setup.bash
ros2 launch my_dual_robot_cell_moveit_config bringup.launch.py \
  alice_ur_type:=ur10 \
  bob_ur_type:=ur10
```

If you prefer the e-series description instead, use:

```bash
ros2 launch my_dual_robot_cell_moveit_config bringup.launch.py \
  alice_ur_type:=ur10e \
  bob_ur_type:=ur10e
```

Use the same choice consistently with the simulator model you selected.

## Notes

- If planning in RViz reports missing semantic data, make sure you are launching `my_dual_robot_cell_moveit_config bringup.launch.py`, not only `start_robots.launch.py`.
- If the workspace `build/`, `install/`, or `log/` directories were previously created by another user or container, you may need to fix ownership before rebuilding.
- The repository `.gitignore` already ignores `ws/build/`, `ws/install/`, and `ws/log/`.
