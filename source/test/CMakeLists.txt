include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_library(tests utils/utils.cpp test.cpp)

target_link_libraries(tests GTest::gtest_main)

target_include_directories(tests PUBLIC utils)

MESSAGE(STATUS ${PROJECT_SOURCE_DIR})

target_include_directories(tests PUBLIC ${PROJECT_SOURCE_DIR}/source/tokenizer)