# Hands-on with TurtleBot3 — Humble → Jazzy conversion

Replacements for each slide in `Hands_on_TurtleBot3.pdf`, targeting **ROS 2 Jazzy Jalisco on Ubuntu 24.04 with Gazebo Harmonic**.

---

## What actually changed

| Area | Humble | Jazzy |
|---|---|---|
| Distro path | `/opt/ros/humble` | `/opt/ros/jazzy` |
| Git branch | `-b humble` | `-b jazzy` |
| Simulator | Gazebo Classic 11 (`gazebo_ros`) | Gazebo Harmonic (`ros_gz`) |
| `/cmd_vel` type | `geometry_msgs/Twist` | `geometry_msgs/TwistStamped` |
| RViz config | hand-built path into `turtlebot3_gazebo` | `turtlebot3_bringup rviz2.launch.py` |
| TF tool | `view_frames.py` | `view_frames` |
| `ros2 pkg create` | license optional | warns unless `--license` given |

Launch file **names** are unchanged (`turtlebot3_world.launch.py`, `navigation2.launch.py`), so most of your `ros2 launch` lines survive as-is. The three that need real edits are Step 0, the controller script, and the RViz2 slide.

---

## Slide 4 — Step 0: Prepare Workspace & Dependencies

> Assume ROS 2 **Jazzy** + **Gazebo Harmonic** are already installed (Ubuntu 24.04).

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

Source Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
```

Install the simulation and navigation dependencies:

```bash
sudo apt update
sudo apt install -y \
  ros-jazzy-ros-gz \
  ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
  ros-jazzy-cartographer-ros \
  python3-colcon-common-extensions python3-rosdep
```

`ros-jazzy-ros-gz` pulls in Gazebo Harmonic. Gazebo Classic is **not** available on Ubuntu 24.04 — it reached end of life in January 2025, which is why the simulator stack changed.

---

## Slide 5 — Step 1: Clone TurtleBot3 Repositories

### Clone Core Packages

```bash
cd ~/ros2_ws/src
# Core TurtleBot3 packages (Jazzy branch)
git clone -b jazzy \
  https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b jazzy \
  https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
```

### Clone Simulation Package

```bash
# Gazebo Harmonic simulation for TurtleBot3
git clone -b jazzy \
  https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
```

### Optional — real hardware only

```bash
git clone -b jazzy \
  https://github.com/ROBOTIS-GIT/DynamixelSDK.git
```

**Result:** `turtlebot3`, `turtlebot3_msgs`, and `turtlebot3_simulations` are now in `~/ros2_ws/src`.

> **Shortcut for a lab full of machines:** Jazzy binaries exist, so
> `sudo apt install ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-msgs ros-jazzy-turtlebot3-gazebo`
> skips the clone-and-build entirely. Worth checking with `apt search ros-jazzy-turtlebot3`
> before the session — it saves students a 10-minute build.

---

## Slide 6 — Step 2: Build & Source the Workspace

### Resolve dependencies first

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

### Build with colcon

```bash
cd ~/ros2_ws
colcon build --symlink-install
```

### Source the Overlay

```bash
source ~/ros2_ws/install/setup.bash
```

- Repeat the `source` command in every new terminal (or add it to `~/.bashrc`).
- Set the model once in `~/.bashrc` so students stop forgetting it:
  ```bash
  echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
  ```

---

## Slides 8–13 — ROS 2 Launch Files

**No changes needed.** `LaunchDescription`, `launch_ros.actions.Node`, `generate_launch_description()`, and the `setup.py` `data_files` glob all behave identically in Jazzy.

One small addition for the `setup.py` slide (slide 13) — Jazzy is stricter about package metadata, so make sure `setup.py` also carries a license field:

```python
# Add to imports:
from glob import glob
import os

# Add to data_files in setup():
(os.path.join('share', package_name, 'launch'), glob('launch/*.py')),

# And in setup():
license='Apache-2.0',
```

---

## Slide 15 — Step 3: Launch Simulation

### Start Gazebo Harmonic Simulation Environment

```bash
# Choose the robot model
export TURTLEBOT3_MODEL=burger

# Launch TurtleBot3 World in Gazebo Harmonic
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Command is unchanged, but the window that opens is the **new Gazebo (Harmonic)**, not Gazebo Classic. First launch takes longer while resources are fetched.

Other worlds:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
```

---

## Slide 16 — Step 4: Explore Available ROS 2 Topics

```bash
ros2 topic list
```

Expected topics are the same, **but the type of `/cmd_vel` has changed**:

- `/cmd_vel` — Velocity commands (input) → now **`geometry_msgs/msg/TwistStamped`**
- `/odom` — Odometry data (output)
- `/scan` — Laser scan data
- `/imu` — Inertial measurement unit data
- `/joint_states` — Robot joint states
- `/tf` and `/tf_static` — Transform data

Good live demo to add here:

```bash
ros2 topic type /cmd_vel
ros2 interface show geometry_msgs/msg/TwistStamped
```

---

## Slide 17 — Step 5: Teleoperate the Robot

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Command and key bindings (`W X A D S`) are unchanged. Internally the node now publishes `TwistStamped`.

---

## Slide 18 — Step 6: Monitor Topic Activity

```bash
ros2 topic echo /cmd_vel
ros2 topic echo /odom
```

```bash
rqt_graph
rqt
```

Unchanged. Note that `ros2 topic echo /cmd_vel` output now shows a `header` block above `twist` — a natural place to point out the message change.

---

## Slide 19 — Step 7: Launch RViz2

The old `ros2 pkg prefix turtlebot3_gazebo`/`.rviz` path is fragile on Jazzy. Use the bringup launch file instead:

```bash
# Launch RViz2 with the TurtleBot3 configuration
ros2 launch turtlebot3_bringup rviz2.launch.py

# Or launch bare and add displays manually
ros2 run rviz2 rviz2
```

Key displays to add (unchanged): **TF**, **LaserScan** (`/scan`), **RobotModel**, **Odometry**, **PointCloud2**.

---

## Slide 20 — RViz2 Configuration Tips

Unchanged, with one rename: the goal tool in the Jazzy toolbar is labelled **"2D Goal Pose"** (the Nav2 plugin also exposes it as "Nav2 Goal"), not "2D Nav Goal".

- Global Options → Fixed Frame: `odom`
- LaserScan → Topic `/scan`, Size 0.1 m
- Interactive Markers → **2D Pose Estimate**, **2D Goal Pose**

---

## Slide 21 — Step 8: Additional Exploration Commands

```bash
# View all running nodes
ros2 node list
# View node information
ros2 node info /teleop_keyboard
# View topic message structure
ros2 interface show sensor_msgs/msg/LaserScan
# Monitor specific topic rate
ros2 topic hz /scan
# View TF tree  (note: no .py suffix in Jazzy)
ros2 run tf2_tools view_frames
```

---

## Slide 23 — Step 1: Create a ROS 2 Package

```bash
cd ~/ros2_ws/src
ros2 pkg create turtlebot3_controller \
  --build-type ament_python \
  --license Apache-2.0 \
  --dependencies rclpy geometry_msgs
```

`--license` is new in practice: Jazzy's `ros2 pkg create` emits a warning without it, and `colcon test` complains later.

---

## Slide 24 — Step 2: Controller Script (rewritten for Jazzy)

Create `turtlebot3_controller/circle_controller.py`.

Three things changed from the Humble version:

1. `Twist` → `TwistStamped` (velocity now lives under `msg.twist`, plus a `header`).
2. Publishing once inside `__init__` never worked reliably — the publisher has not finished discovery yet, so the single message is dropped. Use a timer.
3. `linear.x = 1.0` exceeds the burger's maximum of 0.22 m/s; it gets clamped and the circle is not the radius you advertise.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class Circle(Node):
    def __init__(self):
        super().__init__('turtlebot3_controller')
        self.get_logger().info('Node started with turtlebot3_circle')

        self.vel_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

        self.linear_x = 0.15    # m/s   (burger max: 0.22 m/s)
        self.angular_z = 0.5    # rad/s (burger max: 2.84 rad/s)

        radius = self.linear_x / self.angular_z
        self.get_logger().info(f'Radius = {radius:.2f} m')

        self.timer = self.create_timer(0.1, self.publish_velocity)  # 10 Hz
```

---

## Slide 25 — Step 2 continued

```python
    def publish_velocity(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x = self.linear_x
        msg.twist.angular.z = self.angular_z
        self.vel_pub.publish(msg)

    def stop(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        self.vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Circle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
```

- **Publisher:** publishes `TwistStamped` velocity commands to `/cmd_vel`.
- **Velocity setup:** `twist.linear.x` controls forward speed, `twist.angular.z` the rotation rate.
- **Radius:** r = v / ω, so 0.15 / 0.5 = 0.3 m.
- Stopping on `Ctrl+C` matters — otherwise the robot keeps circling after the node dies.

---

## New slide worth adding — `setup.py` entry point

The original deck never shows this, but `ros2 run turtlebot3_controller circle_controller` fails without it:

```python
entry_points={
    'console_scripts': [
        'circle_controller = turtlebot3_controller.circle_controller:main',
    ],
},
```

---

## Slide 26 — Step 3: Build the Package

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select turtlebot3_controller
```

```bash
source ~/ros2_ws/install/setup.bash
```

Unchanged.

---

## Slide 27 — Step 4: Launch Simulation and Run Controller

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

```bash
ros2 run turtlebot3_controller circle_controller
```

**Result:** The TurtleBot3 follows a circular path of radius ≈ 0.3 m in Gazebo Harmonic.

---

## Slide 31 — Nav2 Step 1: Navigation Setup

### Simulation Environment

```bash
# Launch Gazebo Harmonic simulation
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

### Real Robot Environment

```bash
# Launch navigation with pre-built map
ros2 launch nav2_bringup bringup_launch.py \
  use_sim_time:=false \
  map:=$HOME/tb3_world_map.yaml
```

- **Simulation:** `use_sim_time:=True` for the Gazebo clock
- **Real robot:** `use_sim_time:=false` for the system clock
- **Map path:** ensure the path to your saved map file is correct

> You need a map before this step. Build one with:
> ```bash
> ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
> ros2 run nav2_map_server map_saver_cli -f ~/map
> ```

---

## Slide 32 — Nav2 Step 2: Launch Navigation Stack

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  use_sim_time:=True \
  map:=$HOME/map.yaml
```

Components launched (unchanged): AMCL localization, global + local planners, DWB controller, behavior trees.

**Add this note to the slide:** Nav2 on Jazzy publishes `TwistStamped` on `/cmd_vel` by default. If you are mixing in a node that expects plain `Twist`, set `enable_stamped_cmd_vel: false` in the parameter files of both `turtlebot3_bringup` and `turtlebot3_navigation2`. Keeping the whole stack on one convention avoids a silent "robot never moves" failure.

---

## Slides 33–34 — Set Initial Pose and Navigation Goal

Substantively unchanged. Only the toolbar label for the goal tool differs:

- **2D Pose Estimate** — same name, same behaviour
- **2D Goal Pose** — this was "2D Nav Goal" in the Humble-era RViz2

Troubleshooting notes on both slides still apply.

---

## Slide 35 — Monitor Robot Motion

Unchanged. `rqt` tools (Topic Monitor, Node Graph, Bag Recording, Plotting, Console, Robot Steering) and the RViz2 displays (Map, Path, LaserScan, TF, Costmaps) all work the same.

One caveat for **Robot Steering** in rqt: it publishes plain `Twist`, so on Jazzy it will not drive the robot unless you have switched the stack to `enable_stamped_cmd_vel: false`. Either mention it or drop it from the list.
