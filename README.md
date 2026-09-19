# ROS Workshop Project Overview

## Workshop labels

### Day 1: AMR model and simulation

- `amr_description`: URDF robot model, links, joints, meshes, and RViz visualization.
- `amr_gazebo`: Gazebo world, robot spawning, simulation launch, and ROS/Gazebo bridging.
- `amr_handler`: differential-drive control, wheel odometry, and circular motion.

### Day 2: ROS 2 communication and TurtleBot3 control

- `workshop_demo`: beginner publisher/subscriber examples using ROS 2 topics.
- `turtlebot3_controller`: TurtleBot3 `/cmd_vel` controller that continuously drives a circle in simulation.
- `my_first_package`: generated ROS 2 Python package scaffold for future exercises.

Each folder is a separate ROS 2 package. The package README files and source names provide the code labels; the sections below explain the theory, purpose, and function of each part.

This project is a compact ROS 2 learning workspace for a mobile robot (AMR) and a robotics simulation setup. It is organized as a set of ROS packages, each responsible for one layer of the system:

- robot description and visualization
- Gazebo simulation
- motion control and wheel odometry
- simple ROS topic examples

The structure is intentionally modular so each package does one clear job. This keeps the system measurable and easy to extend for tutorials, experiments, and robot logic.

---

## 1. Project goal

The project teaches the core ideas behind mobile robot software in ROS 2:

- how a robot model is defined in URDF
- how a robot is visualized in RViz
- how simulation is launched in Gazebo
- how wheel commands are converted into motion
- how wheel joint states are used to estimate pose and velocity
- how ROS topics connect publishers and subscribers

The overall pipeline is:

1. A robot description defines the physical robot
2. A launch file publishes the robot state and visualization data
3. A control node sends velocity commands to the robot
4. The odometry node estimates position and orientation from wheel motion
5. The system can be used with RViz and Gazebo for debugging and testing

---

## 2. Folder structure and purpose

The workspace contains these major folders:

### [ros_workshop/amr_description](amr_description)
This package stores the robot’s geometry and visual description. It contains:

- URDF files describing the robot body and joints
- launch files to view the robot in RViz
- meshes and visualization assets

This is the robot “blueprint.” ROS does not move hardware by itself—first it must know the robot structure.

### [ros_workshop/amr_gazebo](amr_gazebo)
This package connects the robot description with Gazebo simulation. It contains:

- Gazebo launch files
- world files
- bridge configuration for ROS/Gazebo communication
- RViz configuration for simulation view

This is how we run the robot in a virtual environment before using it on hardware.

### [ros_workshop/amr_handler](amr_handler)
This is the behavioral package. It contains the actual control logic:

- differential drive command conversion
- wheel odometry estimation
- circular motion pattern node

This is the part that turns motion commands into real robot actions.

### [ros_workshop/workshop_demo](workshop_demo)
This is a minimal tutorial package used to demonstrate ROS publisher/subscriber concepts. It is smaller and easier to understand than the main AMR logic.

---

## 3. Why this design is important

A clean ROS project follows layered design:

- Description layer: what the robot is
- Simulation layer: how the robot behaves in a virtual world
- Control layer: how the robot responds to commands
- Demo layer: how learning examples are kept simple and readable

This separation is important because it makes debugging easier. If the robot does not move correctly, you can isolate the problem to:

- URDF definition
- launch configuration
- joint state source
- wheel command conversion
- odometry estimation

---

## 4. File-by-file explanation

## [ros_workshop/amr_description/launch/display.launch.py](amr_description/launch/display.launch.py)

### Function
This file launches a visualization environment for the AMR robot.

### What it does
- loads the robot model from the URDF file
- publishes the robot state with `robot_state_publisher`
- optionally launches `joint_state_publisher_gui`
- starts RViz2 with a saved configuration

### Why this matters
Robot geometry alone is useless without a way to visualize it. RViz loads the robot description and shows the robot model, helping you inspect the coordinate frames and joint layout.

### ROS theory behind it
`robot_state_publisher` takes the URDF and the current joint states and computes the transforms between robot links. This creates the TF tree that RViz uses to draw the robot.

The joint state publisher is responsible for feeding joint positions into the system. In simulation, those values come from Gazebo or a controller. In visualization, they can also be generated manually using a GUI.

---

## [ros_workshop/amr_description/urdf/amr.urdf](amr_description/urdf/amr.urdf)

### Function
This is the robot model file: the digital skeleton of the robot.

### What it contains
This file defines:

- links such as `base_link`, `chassis_link`, `wheel_left_link`, etc.
- joints such as fixed joints, continuous wheel joints, and sensor mounts
- inertial properties like mass and inertia
- visual meshes and collision geometry

### Why it matters
The robot cannot be controlled in a realistic ROS pipeline unless it has a consistent model. The URDF tells ROS:

- where the wheels are placed
- what the robot coordinate frames are
- which locations are static and which move
- how the robot body is shaped for visualization and simulation

### Theory
A URDF is the canonical robot description format in ROS 2. It defines a tree of links and joints. The `joint_state_publisher` and `robot_state_publisher` together use the URDF to understand the robot’s motion and transform graph.

---

## [ros_workshop/amr_gazebo/launch/gazebo.launch.py](amr_gazebo/launch/gazebo.launch.py)

### Function
This file starts a Gazebo simulation of the AMR.

### What it does
- selects the robot model file
- selects the Gazebo world
- launches `gz_sim`
- spawns the AMR model into the simulation
- bridges ROS topics to Gazebo topics
- optionally launches RViz

### Why this matters
Gazebo gives a safe environment to test robot motion without real hardware. It is often the first stage of validating navigation, control, and sensor logic.

### ROS theory behind it
This file combines several ROS 2 concepts:

- launch files organize the startup sequence
- nodes run independently and connect through topics
- `ROS-Gazebo bridge` translates between ROS messages and Gazebo topics
- TF frames from the robot model are used for simulation and monitoring

This is exactly how ROS 2 enables simulation-first robot development.

---

## [ros_workshop/amr_handler/setup.py](amr_handler/setup.py)

### Function
This file declares the Python package and defines executable entry points.

### What it does
- tells ROS which Python modules belong to this package
- exposes console commands such as:
  - `diff_drive_node`
  - `odometry_node`
  - `circle_motion_node`

### Why this matters
In ROS 2, a node is usually launched as an executable command. This file maps the Python class to an executable name so you can run:

```bash
ros2 run amr_handler diff_drive_node
```

### Theory
The ROS package system uses `setup.py` and `package.xml` to install executables, metadata, and resources in the proper workspace locations. Without this step, your Python nodes would not be launchable through `ros2 run`.

---

## [ros_workshop/amr_handler/amr_handler/diff_drive_node.py](amr_handler/amr_handler/diff_drive_node.py)

### Function
This node converts a desired robot velocity command into wheel commands.

### What it does
- subscribes to `/cmd_vel`
- computes left and right wheel speeds from linear and angular velocity
- clamps the results to safe limits
- publishes to wheel command topics

### Core equation
For a differential drive robot:

- linear velocity: $v$
- angular velocity: $\omega$
- wheel separation: $L$
- wheel radius: $r$

The wheel angular speeds are:

$$
\omega_{left} = \frac{v + \omega \cdot L/2}{r}
$$

$$
\omega_{right} = \frac{v - \omega \cdot L/2}{r}
$$

This is the standard kinematic relationship for a two-wheel differential drive robot.

### Why this matters
A robot does not understand abstract velocity commands directly. It understands wheel motion. This node converts high-level commands like “move forward at 0.2 m/s and turn at 0.5 rad/s” into a concrete left/right motor command set.

### ROS theory behind it
This is a classic publisher/subscriber pattern:

- `/cmd_vel` is the input topic
- wheel command topics are the output topics
- each wheel speed message is a `std_msgs/msg/Float64`

The node acts as a controller interface between motion planning and low-level hardware.

---

## [ros_workshop/amr_handler/amr_handler/odometry_node.py](amr_handler/amr_handler/odometry_node.py)

### Function
This node estimates the robot’s position and orientation from wheel encoder motion.

### What it does
- listens to `/joint_states`
- extracts wheel joint positions
- calculates wheel deltas over time
- converts wheel motion into robot motion
- publishes `/odom`
- broadcasts the transform from `odom` to `base_link`

### Why this matters
A robot must know where it is. Odometry is the basic way of estimating motion using the robot’s own sensors or wheel joints.

### Kinematic ideas
The robot’s motion is estimated from wheel displacement:

- left wheel displacement and right wheel displacement are converted into forward distance and angular rotation
- the robot pose is updated using dead reckoning

The approximate update is:

$$
\Delta d = \frac{\Delta s_{left} + \Delta s_{right}}{2}
$$

$$
\Delta \theta = \frac{\Delta s_{left} - \Delta s_{right}}{L}
$$

where:

- $\Delta d$ is the forward translation
- $\Delta \theta$ is the heading change
- $L$ is wheel separation

Then the new pose is estimated using the current pose and these deltas.

### ROS theory behind it
ROS uses the `nav_msgs/Odometry` message to provide pose and velocity information, and TF transforms to express frame relationships. The node publishes:

- `/odom` for pose and twist information
- `odom -> base_link` transform for tf tree consistency

This is a foundational concept for navigation, mapping, and localization.

---

## [ros_workshop/amr_handler/amr_handler/circle_motion_node.py](amr_handler/amr_handler/circle_motion_node.py)

### Function
This node demonstrates circular motion by continuously publishing a constant twist message.

### What it does
- creates a publisher for `/cmd_vel`
- sets `linear.x` and `angular.z` constant values
- repeats the message at a fixed timer interval
- stops the robot after a configured duration

### Why this matters
This is a simple way to test motion control without writing a full trajectory planner. It demonstrates how a node can command the robot to follow a circular path.

### Theory behind the pattern
A twist message contains both linear and angular motion in a single package:

```python
message.linear.x = 0.2
message.angular.z = 0.5
```

This means the robot will move forward while turning, which results in a curved path. If the forward speed is constant and angular velocity is constant, the motion follows a circle.

The radius of that circle is approximated by:

$$
R = \frac{v}{\omega}
$$

This is a very useful motion-control concept for trajectory testing and mobile robot calibration.

---

## [ros_workshop/workshop_demo/workshop_demo/talker.py](workshop_demo/workshop_demo/talker.py)

### Function
This file is a minimal ROS 2 publisher example.

### What it does
- creates a node called `talker`
- publishes an `Int32MultiArray` to the topic `numbers`
- sends a fixed array every second

### Why this matters
This is one of the earliest beginner examples in ROS 2. It teaches the simplest form of the ROS communication model:

- a node writes data to a topic
- another node can subscribe and read it

### ROS theory behind it
This demonstrates the basic publish-subscribe model:

- publisher node writes to a topic
- topic is a message bus
- subscriber node receives the message asynchronously

It is intentionally simple because it isolates the communication pattern from robot physics or navigation logic.

---

## 5. Relationship between all files

The project works as a pipeline:

1. The URDF defines the robot structure
2. RViz displays the robot in a coordinate system
3. Gazebo simulates the robot and publishes joint states
4. `diff_drive_node` converts the target velocity into joint commands
5. `odometry_node` estimates robot pose from wheel motion
6. `circle_motion_node` demonstrates a continuous mobile motion command
7. `talker.py` introduces the general ROS topic model used throughout the system

This is a very typical ROS 2 robotics stack: description, simulation, control, and messaging.

---

## 6. How the robot motion works in practical terms

The motion stack follows a clean sequence:

### Command layer
A user or node publishes to `/cmd_vel`.

### Controller layer
`diff_drive_node` reads this command and converts it to wheel speeds.

### Actuator layer
The wheel joint command topics are used by the simulation or hardware controller.

### Feedback layer
The wheel joint states are observed and processed by `odometry_node`.

### State estimation layer
The robot’s pose is updated in the `odom` frame.

This is the core logic behind mobile robot control.

---

## 7. Why the project is valuable for learning

This project is useful because it teaches the actual mental model of ROS 2 robotics:

- messages carry data between nodes
- topics are communication channels
- TF frames define the robot’s coordinate system
- URDF defines structure
- control nodes convert commands into lower-level actions
- state estimation reconstructs motion from sensor or joint feedback

This is the same pattern used in real autonomous robots, drones, manipulators, and mobile platforms.

---

## 8. Recommended learning order

1. Read the URDF and understand links and joints
2. Launch the visualization and inspect frames in RViz
3. Run Gazebo and observe the robot in simulation
4. Study `diff_drive_node` and the wheel kinematics
5. Study `odometry_node` and `odom` generation
6. Run the circular motion example
7. Build the simple publisher/subscriber demo

This sequence moves from structure to motion to feedback to communication.

---

## 9. Best practices to keep this project neat

- keep each package focused on one concern
- do not mix simulation logic and low-level control logic in the same file
- keep launch files simple and readable
- keep physical constants such as wheel radius and separation centralized
- name topics and frames clearly
- use consistent frame names: `base_link`, `odom`, `world`

---

## 10. Final takeaway

This project is a practical ROS 2 tutorial for autonomous mobile robot software. It shows how a robot is represented, simulated, controlled, and localized. It compresses the full robotics workflow into a small and understandable package structure.

The key principle is that robotics software is not just “code.” It is a layered system made of:

- description
- simulation
- control
- state estimation
- message passing

That is the real theory behind what we are doing here.
