#include "numbers.hpp"
#include "faker-cxx/number.h"
#include <cstdint>

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
    D_ASSERT(output.ColumnCount() == 1);
    auto &state = input.global_state->Cast<RandomIntGlobalState>();

    if (state.is_finished) {
        output.SetCardinality(0);
    } else {
        const idx_t cardinality = 10;
        output.SetCardinality(cardinality);
        for (idx_t row = 0; row < cardinality; row++) {
            const int32_t random_num = faker::number::integer(0, 100);
            output.SetValue(0, row, Value(random_num));
        }
        state.is_finished = true;
    }

    return OperatorResultType::FINISHED;
}

} // namespace duckdb_faker
