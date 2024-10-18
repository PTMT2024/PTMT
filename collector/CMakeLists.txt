include(CMakePrintHelpers)

set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)

cmake_print_variables(CMAKE_BUILD_TYPE)

cmake_minimum_required(VERSION 3.5.1)
project(mldpp_metrics_collector)

set(CMAKE_CXX_STANDARD 17)

IF(CMAKE_BUILD_TYPE STREQUAL Debug)
        set(CMAKE_C_FLAGS "-lm -Wall -Wpedantic -Winline -Wextra -Wno-long-long -Werror -g -O0 -w -fPIC -mcmodel=medium -fsanitize=address -static-libasan -fno-omit-frame-pointer")
ELSE()
        set(CMAKE_C_FLAGS "-lm -Wall -Wpedantic -Winline -Wextra -Wno-long-long -Werror -g -O2 -w -fPIC -mcmodel=medium")
ENDIF()

#set(CMAKE_C_FLAGS "-g -w -O2 -fPIC")
set(PCM_PATH "/home/sherry/projects/pcm")

include_directories(/usr/local/include)
include_directories(${PCM_PATH}/src)
link_directories(${PCM_PATH}/build/lib)


IF(CMAKE_BUILD_TYPE STREQUAL Debug)
        ADD_DEFINITIONS(-DDEBUG)
ENDIF()

add_executable(mldpp_metrics_collector
        metrics.cc
)


IF(CMAKE_BUILD_TYPE STREQUAL Debug)
        target_compile_options(mldpp_metrics_collector PRIVATE -fsanitize=address)
        target_link_options(mldpp_metrics_collector PRIVATE -fsanitize=address)
ENDIF()

target_link_libraries(mldpp_metrics_collector pfm pcm)


