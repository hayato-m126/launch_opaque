cmake_minimum_required(VERSION 3.14)
project(launch_opaque)

find_package(ament_cmake_python REQUIRED)
find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
  find_package(ament_cmake_pytest)
  ament_add_pytest_test(launch_opaque
    test
  )
endif()

# ament_python_install_package(${PROJECT_NAME})
# install(PROGRAMS
#   DESTINATION lib/${PROJECT_NAME}
# )

ament_auto_package(INSTALL_TO_SHARE
  launch
)
