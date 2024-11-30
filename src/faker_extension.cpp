#define DUCKDB_EXTENSION_MAIN

#include "faker_extension.hpp"
#include "duckdb.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/common/string_util.hpp"
#include "duckdb/function/scalar_function.hpp"
#include "duckdb/main/extension_util.hpp"
#include <duckdb/parser/parsed_data/create_scalar_function_info.hpp>

#include "faker-cxx/person.h"

namespace duckdb {

inline void QuackScalarFun(DataChunk &args, ExpressionState &_, Vector &result) {
	D_ASSERT(args.ColumnCount() == 0);

    result.SetVectorType(VectorType::CONSTANT_VECTOR);

	const auto personFullName = faker::person::fullName();
    result.SetValue(0, duckdb::Value("Quack " + personFullName + " 🐥"));
}

static void LoadInternal(DatabaseInstance &instance) {
    // Register a scalar function
    auto quack_scalar_function = ScalarFunction("quack", {}, LogicalType::VARCHAR, QuackScalarFun);
    ExtensionUtil::RegisterFunction(instance, quack_scalar_function);
}

void FakerExtension::Load(DuckDB &db) {
	LoadInternal(*db.instance);
}
std::string FakerExtension::Name() {
	return "quack";
}

std::string FakerExtension::Version() const {
#ifdef EXT_VERSION_QUACK
	return EXT_VERSION_QUACK;
#else
	return "";
#endif
}

} // namespace duckdb

extern "C" {

DUCKDB_EXTENSION_API void faker_init(duckdb::DatabaseInstance &db) {
    duckdb::DuckDB db_wrapper(db);
    db_wrapper.LoadExtension<duckdb::FakerExtension>();
}

DUCKDB_EXTENSION_API const char *faker_version() {
	return duckdb::DuckDB::LibraryVersion();
}
}

#ifndef DUCKDB_EXTENSION_MAIN
#error DUCKDB_EXTENSION_MAIN not defined
#endif
