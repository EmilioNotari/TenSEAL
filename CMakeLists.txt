cmake_minimum_required(VERSION 3.14)

project(tenseal)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(SEAL_DIR /home/enotari/Escritorio/SEAL/)  #AÑADIDO POR MI

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${SEAL_DIR}/native/src) #AÑADIDO POR MI

if(WIN32)
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
endif()

include(cmake/seal.cmake)
include(cmake/protobuf.cmake)
include(cmake/pybind11.cmake)
include(cmake/xtensor.cmake)
include(cmake/tenseal.cmake)
include(cmake/tests.cmake)

target_link_libraries(tenseal PUBLIC seal) #AÑADIDO POR MI
