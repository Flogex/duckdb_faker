//===----------------------------------------------------------------------===//
//                         DuckDB
//
// function/scalar/system_functions.hpp
//
//
//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_functions.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/function/function_set.hpp"

namespace duckdb {

struct FinalizeFun {
	static constexpr const char *Name = "finalize";
	static constexpr const char *Parameters = "col0";
	static constexpr const char *Description = "";
	static constexpr const char *Example = "";

	static ScalarFunction GetFunction();
};

struct CombineFun {
	static constexpr const char *Name = "combine";
	static constexpr const char *Parameters = "col0,col1";
	static constexpr const char *Description = "";
	static constexpr const char *Example = "";

	static ScalarFunction GetFunction();
};

} // namespace duckdb
