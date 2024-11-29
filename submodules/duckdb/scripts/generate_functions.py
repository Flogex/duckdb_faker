import os
import json
from pathlib import Path


function_groups = {
    ('src', 'include/duckdb', 'function'): ['scalar', 'aggregate'],
    ('extension', 'core_functions/include', 'core_functions'): ['scalar', 'aggregate'],
}


def get_header():
    return '''//===----------------------------------------------------------------------===//
//                         DuckDB
//
// {HEADER}_functions.hpp
//
//
//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_functions.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/function/function_set.hpp"

namespace duckdb {

'''


def get_footer():
    return '''} // namespace duckdb
'''


def main():
    function_type_set = {}
    for (root, include_dir, group), function_types in sorted(function_groups.items()):
        all_functions_group = []
        group_dir = Path(group)
        for function_type in function_types:
            type_dir = Path(root).joinpath(group_dir.joinpath(function_type))
            relative_function_paths = sorted(
                [f'{group}/{function_type}/{f.name}' for f in type_dir.iterdir() if f.is_dir()]
            )
            for function_path in relative_function_paths:
                if Path(normalize_path_separators(f'{root}/{function_path}/functions.json')).exists():
                    create_header_file(root, include_dir, function_path, all_functions_group, function_type_set)
        create_function_list_file(root, group, all_functions_group)


def normalize_path_separators(x):
    return os.path.sep.join(x.split('/'))


def legal_struct_name(name):
    return name.isalnum()


def get_struct_name(function_name):
    return function_name.replace('_', ' ').title().replace(' ', '') + 'Fun'


def get_parameter_line(variants):
    return "\\1".join(
        ",".join(
            param['name'] + "::" + param['type'] if ('type' in param) else param['name']
            for param in variant['parameters']
        )
        for variant in variants
    )


def get_description_line(variants):
    return "\\1".join([variant['description'] for variant in variants])


def get_example_line(variants):
    return "\\1".join([example_from_json(variant) for variant in variants])


def example_from_json(json_record):
    if 'example' in json_record:
        example_line = sanitize_string(json_record['example'])
    elif 'examples' in json_record:
        example_line = examples_to_line(json_record['examples'])
    else:
        example_line = ''
    return example_line


def examples_to_line(example_list):
    return "\\2".join([sanitize_string(example) for example in example_list])


def sanitize_string(text):
    return text.replace('\\', '\\\\').replace('"', '\\"')


def create_header_file(root, include_dir, path, all_function_list, function_type_set):
    header_path = normalize_path_separators(f'{root}/{include_dir}/{path}_functions.hpp')
    json_path = normalize_path_separators(f'{root}/{path}/functions.json')
    with open(json_path, 'r') as f:
        parsed_json = json.load(f)
    new_text = get_header().replace('{HEADER}', path)
    for entry in parsed_json:
        function_text = ''
        if 'struct' in entry:
            struct_name = entry['struct']
        else:
            struct_name = get_struct_name(entry['name'])
        if not legal_struct_name(struct_name):
            print(f'Struct name {struct_name} is not a valid struct name!')
            exit(1)
        if struct_name in function_type_set:
            raise Exception("Duplicate entry " + struct_name)
        function_type_set[struct_name] = entry['type']
        if entry['type'] == 'scalar_function':
            function_text = 'static ScalarFunction GetFunction();'
            all_function_list.append([entry['name'], f"DUCKDB_SCALAR_FUNCTION({struct_name})"])
        elif entry['type'] == 'scalar_function_set':
            function_text = 'static ScalarFunctionSet GetFunctions();'
            all_function_list.append([entry['name'], f"DUCKDB_SCALAR_FUNCTION_SET({struct_name})"])
        elif entry['type'] == 'aggregate_function':
            function_text = 'static AggregateFunction GetFunction();'
            all_function_list.append([entry['name'], f"DUCKDB_AGGREGATE_FUNCTION({struct_name})"])
        elif entry['type'] == 'aggregate_function_set':
            function_text = 'static AggregateFunctionSet GetFunctions();'
            all_function_list.append([entry['name'], f"DUCKDB_AGGREGATE_FUNCTION_SET({struct_name})"])
        else:
            print("Unknown entry type " + entry['type'] + ' for entry ' + struct_name)
            exit(1)
        if 'variants' in entry:
            parameter_line = get_parameter_line(entry['variants'])
            description_line = get_description_line(entry['variants'])
            example_line = get_example_line(entry['variants'])
        else:
            parameter_line = entry['parameters'] if 'parameters' in entry else ''
            description_line = sanitize_string(entry['description'])
            example_line = example_from_json(entry)
        if 'extra_functions' in entry:
            for func_text in entry['extra_functions']:
                function_text += '\n	' + func_text
        new_text += (
            '''struct {STRUCT} {
	static constexpr const char *Name = "{NAME}";
	static constexpr const char *Parameters = "{PARAMETERS}";
	static constexpr const char *Description = "{DESCRIPTION}";
	static constexpr const char *Example = "{EXAMPLE}";

	{FUNCTION}
};

'''.replace(
                '{STRUCT}', struct_name
            )
            .replace('{NAME}', entry['name'])
            .replace('{PARAMETERS}', parameter_line)
            .replace('{DESCRIPTION}', description_line)
            .replace('{EXAMPLE}', example_line)
            .replace('{FUNCTION}', function_text)
        )
        alias_count = 1
        if 'aliases' in entry:
            for alias in entry['aliases']:
                alias_struct_name = get_struct_name(alias)
                if not legal_struct_name(alias_struct_name):
                    alias_struct_name = struct_name + 'Alias'
                    if alias_count > 1:
                        alias_struct_name += str(alias_count)
                    alias_count += 1

                aliased_type = entry['type']
                if aliased_type == 'scalar_function':
                    all_function_list.append([alias, f"DUCKDB_SCALAR_FUNCTION_ALIAS({alias_struct_name})"])
                elif aliased_type == 'scalar_function_set':
                    all_function_list.append([alias, f"DUCKDB_SCALAR_FUNCTION_SET_ALIAS({alias_struct_name})"])
                elif aliased_type == 'aggregate_function':
                    all_function_list.append([alias, f"DUCKDB_AGGREGATE_FUNCTION_ALIAS({alias_struct_name})"])
                elif aliased_type == 'aggregate_function_set':
                    all_function_list.append([alias, f"DUCKDB_AGGREGATE_FUNCTION_SET_ALIAS({alias_struct_name})"])
                else:
                    print("Unknown entry type " + aliased_type + ' for entry ' + struct_name)
                    exit(1)
                function_type_set[alias_struct_name] = aliased_type
                new_text += (
                    '''struct {STRUCT} {
	using ALIAS = {ALIAS};

	static constexpr const char *Name = "{NAME}";
};

'''.replace(
                        '{STRUCT}', alias_struct_name
                    )
                    .replace('{NAME}', alias)
                    .replace('{ALIAS}', struct_name)
                )
    new_text += get_footer()
    with open(header_path, 'w+') as f:
        f.write(new_text)


def create_function_list_file(root, group, all_function_list):
    function_list_file = normalize_path_separators(f'{root}/{group}/function_list.cpp')
    with open(function_list_file, 'r') as f:
        text = f.read()

    static_function = f'static const StaticFunctionDefinition {group}[]' ' = {'
    pos = text.find(static_function)
    header = text[:pos]
    footer_lines = text[pos:].split('\n')
    footer = ''
    for i in range(len(footer_lines)):
        if len(footer_lines[i]) == 0:
            footer = '\n'.join(footer_lines[i:])
            break

    new_text = header
    new_text += static_function + '\n'
    all_function_list = sorted(all_function_list, key=lambda x: x[0])
    for entry in all_function_list:
        new_text += '\t' + entry[1] + ',\n'
    new_text += '\tFINAL_FUNCTION\n};\n'
    new_text += footer

    with open(function_list_file, 'w+') as f:
        f.write(new_text)


if __name__ == "__main__":
    main()
