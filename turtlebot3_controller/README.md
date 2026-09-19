# turtlebot3_controller

A ROS 2 Python package from the TurtleBot3 workshop exercise. It publishes a constant forward and rotational velocity so the robot follows a circular path.

## Build

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --base-paths src --symlink-install --packages-select turtlebot3_controller
source ~/ros2_ws/install/setup.bash
```

## Run with TurtleBot3 simulation

In one terminal:

```bash
source ~/ros2_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

In another terminal:

```bash
source ~/ros2_ws/install/setup.bash
ros2 run turtlebot3_controller circle_controller
```

On ROS 2 Jazzy, `/cmd_vel` uses `geometry_msgs/msg/TwistStamped`; the controller
publishes at 10 Hz and sends a zero command when it shuts down.
