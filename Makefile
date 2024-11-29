PROJ_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# Configuration of extension
EXT_NAME=quack
EXT_CONFIG=${PROJ_DIR}extension_config.cmake

DUCKDB_SRCDIR := ./submodules/duckdb/

# Include the Makefile from extension-ci-tools
include submodules/extension-ci-tools/makefiles/duckdb_extension.Makefile