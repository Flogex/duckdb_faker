#include "duckdb/main/extension_util.hpp"
#include "duckdb/main/database.hpp"

#include "duckdb/common/vector.hpp"
#include "duckdb/function/function.hpp"
#include "duckdb/function/table_function.hpp"
#include "duckdb/common/types.hpp"
#include "duckdb/common/types/data_chunk.hpp"
#include "numbers.hpp"
#include "faker-cxx/number.h"
#include <cstdint>
#include <limits>
#include <optional>

using namespace duckdb;

namespace duckdb {
class ClientContext;
}

namespace duckdb_faker {

namespace {
struct RandomIntFunctionData final : TableFunctionData {
    std::optional<int32_t> min;
    std::optional<int32_t> max;
};

struct RandomIntGlobalState final : GlobalTableFunctionState {
    uint64_t generated_rows = 0;
    bool is_finished = false;
};

unique_ptr<FunctionData> RandomIntBind(ClientContext &, TableFunctionBindInput &input, vector<LogicalType> &return_types,
                                       vector<string> &names) {
    return_types.push_back(LogicalType::INTEGER);
    names.push_back("value");

    auto bind_data = make_uniq<RandomIntFunctionData>();
    if (input.named_parameters.contains("min")) {
        bind_data->min = input.named_parameters["min"].GetValue<int32_t>();
    }
    if (input.named_parameters.contains("max")) {
        bind_data->max = input.named_parameters["max"].GetValue<int32_t>();
    }

    return bind_data;
}

unique_ptr<GlobalTableFunctionState> RandomIntGlobalInit(ClientContext &, TableFunctionInitInput &) {
    return make_uniq<RandomIntGlobalState>();
}

void RandomIntExecute(ClientContext &, TableFunctionInput &input, DataChunk &output) {
    D_ASSERT(output.ColumnCount() == 1);
    auto &state = input.global_state->Cast<RandomIntGlobalState>();

    if (state.is_finished) {
        output.SetCardinality(0);
        return;
    }

    const auto &bind_data = input.bind_data->Cast<RandomIntFunctionData>();
    const int32_t min = bind_data.min.value_or(std::numeric_limits<int32_t>::min());
    const int32_t max = bind_data.max.value_or(std::numeric_limits<int32_t>::max());

    const idx_t cardinality = DEFAULT_MAX_GENERATED_ROWS;
    output.SetCardinality(cardinality);
    while (state.generated_rows < cardinality) {
        const idx_t row = state.generated_rows;
        const int32_t random_num = faker::number::integer(min, max);
        output.SetValue(0, row, Value(random_num));
        state.generated_rows++;
    }
    state.is_finished = true;
}
} // anonymous namespace

void RandomIntFunction::RegisterFunction(DatabaseInstance &instance) {
    TableFunction random_int_function("random_int", {}, RandomIntExecute, RandomIntBind, RandomIntGlobalInit);
    random_int_function.named_parameters["min"] = LogicalType::INTEGER;
    random_int_function.named_parameters["max"] = LogicalType::INTEGER;
    ExtensionUtil::RegisterFunction(instance, random_int_function);
}
} // namespace duckdb_faker
