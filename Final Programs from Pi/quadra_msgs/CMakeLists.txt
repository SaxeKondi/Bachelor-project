cmake_minimum_required(VERSION 2.8.3)
project(quadra_msgs)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  rospy
  std_msgs
)

add_message_files(
  DIRECTORY msg
  FILES
    ImpedanceSpectrum.msg
)

generate_messages(
  DEPENDENCIES 
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/listener.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
