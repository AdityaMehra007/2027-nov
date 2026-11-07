cmake_minimum_required(VERSION 3.25)
project(AetherOmegaRTOS VERSION 2027.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler optimization and safety flags
if(MSVC)
    add_compile_options(/O2 /W4 /permissive-)
else()
    add_compile_options(-O3 -march=native -Wall -Wextra -pedantic)
endif()

include_directories(src/rtos src/cislunar src/hardware src/reversible_2085)

# Tokamak Magnetic Confinement Controller Executable
add_executable(tokamak_control src/hardware/tokamak_magnetic_control.cpp)

# Header-only interfaces interface library
add_library(aether_rtos_headers INTERFACE)
target_include_directories(aether_rtos_headers INTERFACE src/rtos src/cislunar src/reversible_2085)
