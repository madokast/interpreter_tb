add_executable(it_test utils/asserts.cpp testentry.cpp)

target_include_directories(it_test PUBLIC utils)

target_include_directories(it_test PUBLIC ${PROJECT_SOURCE_DIR}/src/code/tokenizer)