cmake_minimum_required(VERSION 3.0.2)
project(needle_insertion_robot)


## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  geometry_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  quadra_msgs
)

catkin_package(
  CATKIN_DEPENDS 
  cv_bridge
  geometry_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  quadra_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/tissue_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)














