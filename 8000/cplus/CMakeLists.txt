cmake_minimum_required(VERSION 3.10)
project(INT8QuantizationEngine)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 包含目录
include_directories(${CMAKE_SOURCE_DIR}/include)

# 源文件
set(SOURCES
    src/Tensor.cpp
    src/LinearLayer.cpp
    src/Model.cpp
    src/Utils.cpp
    src/main.cpp
)

# 可执行文件
add_executable(inference_engine ${SOURCES})

# 编译选项
if(MSVC)
    # Visual Studio编译选项
    # /utf-8: 确保源文件中的中文字符串等按 UTF-8 正确解析，避免出现 C2001 等乱码导致的语法错误
    target_compile_options(inference_engine PRIVATE /W4 /utf-8)
else()
    # GCC/Clang编译选项
    target_compile_options(inference_engine PRIVATE -Wall -Wextra -O2)
endif()

# 如果需要C++17文件系统库（某些编译器需要）
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS "9.0")
    target_link_libraries(inference_engine PRIVATE stdc++fs)
endif()
