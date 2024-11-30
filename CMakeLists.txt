cmake_minimum_required(VERSION 3.22)
set (CMAKE_CXX_STANDARD 20)

# Set extension name here
set(TARGET_NAME quack)

set(EXTENSION_NAME ${TARGET_NAME}_extension)
set(LOADABLE_EXTENSION_NAME ${TARGET_NAME}_loadable_extension)

project(${TARGET_NAME})

set(BUILD_TESTING OFF)
add_subdirectory(submodules/faker-cxx)

include_directories(src/include)

set(EXTENSION_SOURCES
    src/quack_extension.cpp)

build_static_extension(${TARGET_NAME} ${EXTENSION_SOURCES})
build_loadable_extension(${TARGET_NAME} " " ${EXTENSION_SOURCES})

include_directories(${TARGET_NAME}
    ${CMAKE_CURRENT_LIST_DIR}/submodules/faker-cxx/include)

# Link OpenSSL in both the static library as the loadable extension
target_link_libraries(${EXTENSION_NAME} faker-cxx)
target_link_libraries(${LOADABLE_EXTENSION_NAME} faker-cxx)


install(
    TARGETS faker-cxx
    EXPORT "${DUCKDB_EXPORT_SET}"
    LIBRARY DESTINATION "${INSTALL_LIB_DIR}"
    ARCHIVE DESTINATION "${INSTALL_LIB_DIR}")

install(
    TARGETS ${EXTENSION_NAME}
    EXPORT "${DUCKDB_EXPORT_SET}"
    LIBRARY DESTINATION "${INSTALL_LIB_DIR}"
    ARCHIVE DESTINATION "${INSTALL_LIB_DIR}")
