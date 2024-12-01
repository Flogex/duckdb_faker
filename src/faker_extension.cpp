#define DUCKDB_EXTENSION_MAIN

#include "faker_extension.hpp"
#include "duckdb/common/types.hpp"
#include "duckdb/main/database.hpp"
#include "duckdb/main/extension_util.hpp"
#include "table_functions/numbers.hpp"

namespace duckdb {

static void RegisterFunctions(DatabaseInstance &instance) {
    TableFunction random_int_function("random_int", {}, nullptr);
    random_int_function.in_out_function = duckdb_faker::RandomIntFunction;
    random_int_function.bind = duckdb_faker::RandomIntBind;
    random_int_function.init_global = duckdb_faker::RandomIntGlobalInit;
    ExtensionUtil::RegisterFunction(instance, random_int_function);
}

void FakerExtension::Load(DuckDB &db) {
    DatabaseInstance &instance = *db.instance;
    RegisterFunctions(instance);
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
