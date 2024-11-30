#pragma once

#include "duckdb/common/enums/operator_result_type.hpp"
#include "duckdb/common/types/data_chunk.hpp"
#include "duckdb/function/table_function.hpp"

namespace duckdb {
    class ClientContext;
}

using namespace duckdb;

namespace duckdb_faker {

struct RandomIntGlobalState final : public GlobalTableFunctionState {
    bool is_finished = false;
};

unique_ptr<GlobalTableFunctionState> RandomIntGlobalInit(ClientContext &context, TableFunctionInitInput &input);
unique_ptr<FunctionData> RandomIntBind(ClientContext &context, TableFunctionBindInput &input,
                                       vector<LogicalType> &return_types, vector<string> &names);
OperatorResultType RandomIntFunction(ExecutionContext &context, TableFunctionInput &data, DataChunk &input,
                                     DataChunk &output);

} // namespace duckdb_faker
