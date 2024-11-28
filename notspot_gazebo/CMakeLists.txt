cmake_minimum_required(VERSION 3.8)
project(notspot_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gazebo REQUIRED)
find_package(gazebo_ros REQUIRED)

set(dependencies
  rclcpp
  gazebo
  gazebo_ros
)

install(DIRECTORY
  launch
  models
  worlds
  DESTINATION share/${PROJECT_NAME}/
)
ament_package()
