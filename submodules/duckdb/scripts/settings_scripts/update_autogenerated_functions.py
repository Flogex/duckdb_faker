from .config import (
    SRC_CODE_START_MARKER,
    SRC_CODE_END_MARKER,
    SettingsList,
    find_start_end_indexes,
    get_setting_heading,
)


def generate_create_value(setting):
    if setting.sql_type == 'VARCHAR':
        return 'Value'
    else:
        return f'Value::{setting.sql_type}'


def add_autogenerated_global_functions(setting):
    cpp_code = ""
    if 'set' not in setting.custom_implementation:
        cpp_code += (
            f"void {setting.struct_name}::SetGlobal(DatabaseInstance *db, DBConfig &config, const Value &input) {{\n"
        )
        if setting.on_set:
            cpp_code += f"\tif (!OnGlobalSet(db, config, input)) {{\n"
            cpp_code += f"\t\treturn;\n\t}}\n"
        if setting.is_enum:
            cpp_code += f"\tauto str_input = StringUtil::Upper(input.GetValue<string>());\n"
            cpp_code += f"\tconfig.options.{setting.internal_setting} = EnumUtil::FromString<{setting.return_type}>(str_input);\n"
        else:
            cpp_code += f"\tconfig.options.{setting.internal_setting} = input.GetValue<{setting.return_type}>();\n"
        cpp_code += f"}}\n\n"
    if 'reset' not in setting.custom_implementation:
        cpp_code += f"void {setting.struct_name}::ResetGlobal(DatabaseInstance *db, DBConfig &config) {{\n"
        if setting.on_reset:
            cpp_code += f"\tif (!OnGlobalReset(db, config)) {{\n"
            cpp_code += f"\t\treturn;\n\t}}\n"
        cpp_code += f"\tconfig.options.{setting.internal_setting} = DBConfig().options.{setting.internal_setting};\n"
        cpp_code += f"}}\n\n"
    if 'get' not in setting.custom_implementation:
        cpp_code += f"Value {setting.struct_name}::GetSetting(const ClientContext &context) {{\n"
        cpp_code += f"\tauto &config = DBConfig::GetConfig(context);\n"
        if setting.is_enum:
            cpp_code += f"\treturn {generate_create_value(setting)}(StringUtil::Lower(EnumUtil::ToString(config.options.{setting.internal_setting})));\n"
        else:
            cpp_code += f"\treturn {generate_create_value(setting)}(config.options.{setting.internal_setting});\n"
        cpp_code += f"}}\n\n"
    return cpp_code


def add_autogenerated_local_functions(setting):
    cpp_code = ""
    if 'set' not in setting.custom_implementation:
        cpp_code += f"void {setting.struct_name}::SetLocal(ClientContext &context, const Value &input) {{\n"
        if setting.on_set:
            cpp_code += f"\tif (!OnLocalSet(context, input)) {{\n"
            cpp_code += f"\t\treturn;\n\t}}\n"
        cpp_code += f"\tauto &config = ClientConfig::GetConfig(context);\n"
        if setting.is_enum:
            cpp_code += f"\tauto str_input = StringUtil::Upper(input.GetValue<string>());\n"
            cpp_code += (
                f"\tconfig.{setting.internal_setting} = EnumUtil::FromString<{setting.return_type}>(str_input);\n"
            )
        else:
            cpp_code += f"\tconfig.{setting.internal_setting} = input.GetValue<{setting.return_type}>();\n"
        cpp_code += f"}}\n\n"
    if 'reset' not in setting.custom_implementation:
        cpp_code += f"void {setting.struct_name}::ResetLocal(ClientContext &context) {{\n"
        if setting.on_reset:
            cpp_code += f"\tif (!OnLocalReset(context)) {{\n"
            cpp_code += f"\t\treturn;\n\t}}\n"
        cpp_code += f"\tClientConfig::GetConfig(context).{setting.internal_setting} = ClientConfig().{setting.internal_setting};\n"
        cpp_code += f"}}\n\n"
    if 'get' not in setting.custom_implementation:
        cpp_code += f"Value {setting.struct_name}::GetSetting(const ClientContext &context) {{\n"
        cpp_code += f"\tauto &config = ClientConfig::GetConfig(context);\n"
        if setting.is_enum:
            cpp_code += f"\treturn {generate_create_value(setting)}(StringUtil::Lower(EnumUtil::ToString(config.{setting.internal_setting})));\n"
        else:
            cpp_code += f"\treturn {generate_create_value(setting)}(config.{setting.internal_setting});\n"
        cpp_code += f"}}\n\n"
    return cpp_code


def add_autogenerated_functions(path):
    with open(path, 'r') as source_file:
        source_code = source_file.read()

    # find start and end indexes of the auto-generated section
    start_index, end_index = find_start_end_indexes(source_code, SRC_CODE_START_MARKER, SRC_CODE_END_MARKER, path)

    # split source code into sections
    start_section = source_code[: start_index + 1] + "\n"
    end_section = source_code[end_index:]

    new_content = ""
    added = 0
    for setting in SettingsList:
        # if the setting doesn't need custom implementation, an autogenerated one will be included
        if not setting.all_custom:
            new_content += get_setting_heading(setting.struct_name)
            if setting.scope == "GLOBAL" or setting.scope == "GLOBAL_LOCAL":
                new_content += add_autogenerated_global_functions(setting)
            if setting.scope == "LOCAL" or setting.scope == "GLOBAL_LOCAL":
                new_content += add_autogenerated_local_functions(setting)
            added += 1
    return start_section + new_content + end_section, added


if __name__ == '__main__':
    raise ValueError("Please use 'generate_settings.py' instead of running the individual script(s)")
