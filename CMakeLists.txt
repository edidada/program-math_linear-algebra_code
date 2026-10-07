cmake_minimum_required(VERSION 3.20)
project(programmers_mathematics_linear_algebra LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(mymatrix mymatrix.cpp)
add_executable(mat_anim mat_anim.cpp)

include(CTest)
if(BUILD_TESTING)
  add_test(NAME matrix_examples COMMAND mymatrix)
endif()
