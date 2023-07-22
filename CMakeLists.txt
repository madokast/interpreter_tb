cmake_minimum_required(VERSION 3.14)
project(interpreter_tb)

# GoogleTest requires at least C++14
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

enable_testing()

add_subdirectory(source/test)

add_executable(test_entry test_entry.cpp)

target_link_libraries(test_entry PUBLIC tests)

include(GoogleTest)
gtest_discover_tests(test_entry)