# turtlebot3_controller

A ROS 2 Python package from the TurtleBot3 workshop exercise. It publishes a constant forward and rotational velocity so the robot follows a circular path.

## Build

```bash
cd ~/ros2_ws/ros_workshop
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select turtlebot3_controller
source install/setup.bash
```

## Run with TurtleBot3 simulation

In one terminal:

```bash
source ~/ros2_ws/ros_workshop/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

In another terminal:

```bash
source ~/ros2_ws/ros_workshop/install/setup.bash
ros2 run turtlebot3_controller circle_controller
```
