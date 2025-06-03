# LAENTIEC-J8_ros2_unity
## Project Documentation: ARGO J8 Robot Simulation in Unity with ROS2
 
## Contents:
This repository contains the Unity Project, the ROS2 work-space and all the required files (textures, models, ect. ect.).

Some **videos** can be seen at https://www.youtube.com/playlist?list=PLzGHhHCD9XWRZUDRAvq-ftrLqUgAzODbC. 

## 1. Introduction
This project aims to simulate the behaviour of an ARGO J8 mobile robot in a virtual environment created within Unity. The simulation enables testing and development of control and perception algorithms in a controlled setting before implementation on the physical robot.

Technologies used:

* **ROS2 Humble**: Robotics framework for creating nodes and inter-node communication.
* **Unity**: Game engine used to create the virtual environment and simulate the robot's physics.
* **ROS-TCP-Connector**: Bridge for communication between ROS2 and Unity.

## 2. Environment Setup
Prerequisites:
* **Operating system**: Linux (Ubuntu 22.04 recommended)
* **ROS2 Humble**: Follow the official installation instructions: https://docs.ros.org/en/humble/Installation.html
* **Unity**: Download and install the version used in the project (2022.3.44f1). It can run on Ubuntu or Windows. https://unity.com/es/download
* **ROS2 package installation**:

 * Clone the ROS2 workspace:

```
git clone https://github.com/Robotics-Mechatronics-UMA/LAENTIEC-J8_ros2_unity.git
cd LAENTIEC-J8_ros2_unity/src 
```
 * Compile the packages:
```
colcon build
```
* **Unity Configuration**:
* Download the folder containing the project: Unity-ROS2-Project. **IMPORTANT**: This repository is being updated. In the meantime, please refer to https://github.com/Kmdnb/TFG_KDN_UnityROS2 for the Unity files.

* Open the Unity project:
 * From Unity Hub - Select "Open project": Once the editor has started, you will see a welcome screen. Look for and select the "Open project" option.
 * Navigate to the folder where the project is downloaded: A file explorer window will open. Navigate to the location where the Unity-ROS2-Project folder is located.
 * Select the folder and open: Once you have located the project folder, select it and click the "Open" button.

## 3. ROS2-Unity Communication
Communication between ROS2 and Unity is established through the ROS-TCP-Connector. ROS2 nodes publish and subscribe to topics to send and receive data. In Unity, scripts handle reading and writing topic data. Follow the steps in the official ROS-TCP-Connector documentation to install and run this package in Unity and ROS2: https://github.com/Unity-Technologies/Unity-Robotics-Hub/tree/main This package includes the URDF Importer for Unity.  

## 4. Unity Preparation
Once the project is open and the ROS-TCP-Connector package is configured, follow these steps to increase the terrain texture resolution:

* Go to Assets >3D Meshes > Textures, and click on the TerrainTexture image.
* Then, change the settings accordingly. Recommended values:
 * Aniso Level = 16
 * Max Size = 16384
 * Compression = High Quality.

## 5. Project Execution
**Starting ROS2**:
* Open several terminals.
* Source the ROS2 setup:
```
source ~/ros2_ws/install/setup.bash
```
* Establish a connection with Unity through ROS-TCP-Connector.
```
ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_IP:= [YOUR_IP]
```
* Run the nodes in different terminals:
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard #Teleoperate
ros2 run camera_subscriber camera_subscriber #Camera view of the ARGO J8
ros2 run lidar_subscriber lidar_subscriber #Lidar response
ros2 run fixposition_pkg gps_subscriber #GPS response
ros2 run fixposition_pkg imu_subscriber #IMU response
ros2 run fixposition_pkg odometry_subscriber #Odometry response
```
**Starting Unity**:

* Run the project scene in Unity

* Verifying the connection:

ROS2: Check that sensor readings are consistent.

Unity: Verify that data is being received and processed correctly in Unity.

## 6. Multimedia
This section includes an image of the robot and the simulated terrain, as well as a video summarizing the simulation's operation.

### Notice:
This is a streamlined version of the original repository at https://github.com/Kmdnb/TFG_KDN_UnityROS2. You can visit it for more details.
