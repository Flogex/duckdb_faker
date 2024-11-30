#include "numbers.hpp"

namespace duckdb_faker {

unique_ptr<GlobalTableFunctionState> RandomIntGlobalInit(ClientContext &, TableFunctionInitInput &) {
    return make_uniq<RandomIntGlobalState>();
}

unique_ptr<FunctionData> RandomIntBind(ClientContext &, TableFunctionBindInput &, vector<LogicalType> &return_types,
                                       vector<string> &names) {
    return_types.push_back(LogicalType::INTEGER);
    names.push_back("value");
    return nullptr;
}

OperatorResultType RandomIntFunction(ExecutionContext &, TableFunctionInput &input, DataChunk &,
                                     DataChunk &output) {
    auto &state = input.global_state->Cast<RandomIntGlobalState>();

    if (state.is_finished) {
        output.SetCardinality(0);
    } else {
        output.SetValue(0, 0, Value(42));
        output.SetCardinality(1);
        state.is_finished = true;
    }

    return OperatorResultType::FINISHED;
}

} // namespace duckdb_faker
