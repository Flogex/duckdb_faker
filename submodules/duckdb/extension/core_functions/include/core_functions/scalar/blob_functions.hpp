//===----------------------------------------------------------------------===//
//                         DuckDB
//
// core_functions/scalar/blob_functions.hpp
//
//
//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_functions.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/function/function_set.hpp"

namespace duckdb {

struct DecodeFun {
	static constexpr const char *Name = "decode";
	static constexpr const char *Parameters = "blob";
	static constexpr const char *Description = "Convert blob to varchar. Fails if blob is not valid utf-8";
	static constexpr const char *Example = "decode('\\xC3\\xBC'::BLOB)";

	static ScalarFunction GetFunction();
};

struct EncodeFun {
	static constexpr const char *Name = "encode";
	static constexpr const char *Parameters = "string";
	static constexpr const char *Description = "Convert varchar to blob. Converts utf-8 characters into literal encoding";
	static constexpr const char *Example = "encode('my_string_with_ü')";

	static ScalarFunction GetFunction();
};

struct FromBase64Fun {
	static constexpr const char *Name = "from_base64";
	static constexpr const char *Parameters = "string";
	static constexpr const char *Description = "Convert a base64 encoded string to a character string";
	static constexpr const char *Example = "from_base64('QQ==')";

	static ScalarFunction GetFunction();
};

struct ToBase64Fun {
	static constexpr const char *Name = "to_base64";
	static constexpr const char *Parameters = "blob";
	static constexpr const char *Description = "Convert a blob to a base64 encoded string";
	static constexpr const char *Example = "base64('A'::blob)";

	static ScalarFunction GetFunction();
};

struct Base64Fun {
	using ALIAS = ToBase64Fun;

	static constexpr const char *Name = "base64";
};

} // namespace duckdb
