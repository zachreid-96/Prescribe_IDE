import os.path
import json, re
import pyparsing as pparser


def load(f):
    if os.path.exists(f):
        with open(f, "r") as params:
            data = json.load(params)
        return data
    return None

_memory = {}
def memoize_command(c):
    def inner(c1):
        if c1 not in _memory:
            _memory[c1] = c(c1)
        return _memory[c1]
    return inner

@memoize_command
def parse_command(c1):
    if c1 == "!R!":
        return True, "Success"
    elif c1 == "EXIT;":
        return True, "Success"

    parsing_gate = Parser()

    delimiters = r',|;|"| '
    tokens = list(filter(None, re.split(delimiters, c1)))

    keyword, parameter, values = None, None, None

    if len(tokens) >= 3:
        keyword = tokens[0]
        parameter = tokens[1]
        values = tokens[2:]

    if keyword == "FRPO":
        parameter_list = parsing_gate.frpo_params
    elif keyword == "KCFG":
        parameter_list = parsing_gate.kcfg_params
    else:
        parameter_list = parsing_gate.prescribe_params
        if keyword not in list(parameter_list.keys()):
            given_tokens = generate_tokens(c1)
            expected_tokens = get_expected_tokens(given_tokens)
            return compare_tokens(expected_tokens, given_tokens)

    param = parameter_list.get(parameter, None)
    if param is None:
        given_tokens = generate_tokens(c1)
        expected_tokens = get_expected_tokens(given_tokens)
        return compare_tokens(expected_tokens, given_tokens)
    command_format = param.get("Format", None)
    if not command_format:
        return False, "Missing Format for Command"
    format_keys = command_format.split(",")
    command_keys = c1.split(",")
    if format_keys[0] == command_keys[0]:
        #print(command_keys)
        if len(command_keys) == 2:
            return handle_command_value_check(values[0], parameter_list[parameter]["Values"][0])
        elif len(command_keys) > 2:
            given_tokens = generate_tokens(c1)
            expected_tokens = get_expected_tokens(given_tokens)
            if parameter_list[parameter].get("Multi-Paramater", 0) == 0:
                return False, "Parameter does not take multiple arguments"
            if parameter_list[parameter].get("Conditional", 0) == 1:
                return compare_tokens(expected_tokens, given_tokens)
            return compare_tokens(expected_tokens, given_tokens)
        else:
            given_tokens = generate_tokens(c1)
            expected_tokens = get_expected_tokens(given_tokens)
            return compare_tokens(expected_tokens, given_tokens)

    given_tokens = generate_tokens(c1)
    expected_tokens = get_expected_tokens(given_tokens)
    return compare_tokens(expected_tokens, given_tokens)

def parse_command_old(c1):
    if c1 == "!R!":
        return True, "Success"
    elif c1 == "EXIT;":
        return True, "Success"

    parsing_gate = Parser()

    delimiters = r',|;|"| '
    tokens = list(filter(None, re.split(delimiters, c1)))

    keyword, parameter, values = None, None, None

    if len(tokens) >= 3:
        keyword = tokens[0]
        parameter = tokens[1]
        values = tokens[2:]

    if keyword == "FRPO":
        parameter_list = parsing_gate.frpo_params
    elif keyword == "KCFG":
        parameter_list = parsing_gate.kcfg_params
    else:
        parameter_list = parsing_gate.prescribe_params
        if keyword not in list(parameter_list.keys()):
            given_tokens = generate_tokens(c1)
            expected_tokens = get_expected_tokens(given_tokens)
            return compare_tokens(expected_tokens, given_tokens)

    param = parameter_list.get(parameter, None)
    if param is None:
        given_tokens = generate_tokens(c1)
        expected_tokens = get_expected_tokens(given_tokens)
        return compare_tokens(expected_tokens, given_tokens)
    command_format = param.get("Format", None)
    if not command_format:
        return False, "Missing Format for Command"
    format_keys = command_format.split(",")
    command_keys = c1.split(",")
    if format_keys[0] == command_keys[0]:
        #print(command_keys)
        if len(command_keys) == 2:
            return handle_command_value_check(values[0], parameter_list[parameter]["Values"][0])
        elif len(command_keys) > 2:
            if parameter_list[parameter].get("Multi-Paramater", 0) == 0:
                return False, "Parameter does not take multiple arguments"
            if parameter_list[parameter].get("Conditional", 0) == 1:
                return handle_multi_conditional_commands(values, parameter_list[parameter]["Values"])
            return handle_mutli_unconditional_commands(values, parameter_list[parameter]["Values"])
        else:
            given_tokens = generate_tokens(c1)
            expected_tokens = get_expected_tokens(given_tokens)
            return compare_tokens(expected_tokens, given_tokens)

    given_tokens = generate_tokens(c1)
    expected_tokens = get_expected_tokens(given_tokens)
    return compare_tokens(expected_tokens, given_tokens)

def get_option_mutli(indx, int_val, check_value):
    pass

def handle_multi_conditional_commands(command_value, check_value):

    for pos, val in enumerate(command_value):
        for option in check_value:
            if option.get("Position", -1) == (pos + 1) and option.get("Type", "") == "enum":
                if option.get("Position", -1) == 1:
                    #print("\t", option)
                    pass
                elif option.get("Parent Position", 0) == pos and str(option.get("Parent Option", -1)) == command_value[pos-1]:
                    #print("\t", option)
                    pass
            elif option.get("Position", -1) == (pos + 1) and option.get("Type", "") == "range":
                if (option.get("Parent Position", 0) == pos and str(option.get("Grandparent Option", -1)) == command_value[pos-2]
                        and str(option.get("Parent Option", -1)) == command_value[pos-1]):
                    #print("\t", option)
                    command_int_value = None
                    try:
                        command_int_value = int(val)
                    except ValueError:
                        return False, f"Unable to parse value {pos + 1} as Integer"
                    if command_int_value is not None:
                        check_min = option["min"]
                        check_max = option["max"]
                        if check_min < command_int_value < check_max:
                            return True, "Success"
                        else:
                            return False, "Value outside of accepted range"
                    else:
                        return False, "Value cannot be None"


    return False, "WIP"

def handle_mutli_unconditional_commands(command_value, check_value):
    _position_count = 0
    for value in check_value:
        if _position_count < value.get("Position", 0):
            _position_count = value.get("Position", 0)

    if _position_count < len(command_value):
        return False, "Missing positional arguments"
    elif _position_count > len(command_value):
        return False, "Too many positinal arguments"



    return False, "Not Implemented Yet"

def handle_command_value_check(command_value, check_value):
    if check_value["Type"] == "enum":
        options = check_value["Options"].keys()
        if command_value in options:
            return True, "Success"
        else:
            return False, "Value not a valid option"
    elif check_value["Type"] == "range":
        return handle_range_value_check(command_value, check_value)
    elif check_value["Type"] == "Integer":
        return handle_integer_value_check(command_value)

    return False, "Unrecognized Command Value Type"

def handle_range_value_check(command_value, check_value):
    command_int_value = None
    try:
        command_int_value = int(command_value)
    except ValueError:
        return False, "Unable to parse as Integer"
    if command_int_value is not None:
        check_min = check_value["min"]
        check_max = check_value["max"]
        if check_min < command_int_value < check_max:
            return True, "Success"
        else:
            return False, "Value outside of accepted range"
    else:
        return False, "Value cannot be None"

def handle_integer_value_check(command_value):
    command_int_value = None
    try:
        command_int_value = int(command_value)
    except ValueError:
        return False, "Unable to parse as Integer"
    if command_int_value and command_int_value >= 0:
        return True, "Success"
    else:
        return False, "Integer value cannot be negative"

def generate_tokens(command):
    parser = Parser()

    available_keywords = parser.available_commands

    tokens = []
    curr_token = ""
    curr_quote_count = 0
    for pos, char in enumerate(command):
        if char == '"':
            curr_quote_count += 1
            if curr_quote_count == 1:
                tokens.append(curr_token)
                curr_token = ""
                curr_token = curr_token + char
            else:
                curr_token = curr_token + char
                tokens.append(curr_token)
                curr_token = ""
                curr_quote_count = 0
        elif char == " " or char == "," or char == ";" or char == "?":
            if curr_token:
                tokens.append(curr_token)
            tokens.append(char)
            curr_token = ""
        else:
            curr_token = curr_token + char
            if curr_token in available_keywords:
                tokens.append(curr_token)
                curr_token = ""
    #print("gen", tokens)
    return tokens

def get_expected_tokens(command):
    parser = Parser()

    if not command:
        return []

    if command[0] == "FRPO":
        parent_commands = parser.frpo_params
        keyword = "FRPO"
    elif command[0] == "KCFG":
        parent_commands = parser.kcfg_params
        keyword = "KCFG"
    else:
        parent_commands = parser.prescribe_params
        keyword = command[0]

    parameter_list = [p.get("Parameter") for p in parent_commands.values()]

    parameter = None
    example_command = None
    for t in command[1:]:
        if t in parameter_list:
            parameter = t
            example_command = parent_commands[t.strip('"')].get("Format")
            break

    tokens = []
    if example_command:
        new_command = re.sub(r"#\d", '?', example_command)
        tokens = generate_tokens(new_command)
    #print("get", tokens)
    return tokens

def compare_tokens(expected, given):
    for pos, (expected_token, given_token) in enumerate(zip(expected, given)):
        if expected_token != given_token and expected_token != "?":
            count = 0
            for token in given[:pos]:
                count += len(token)
            return False, f"Expected '{expected_token}' but got '{given_token}' at position {count}"
    return True, "Success"


def parse_line(full_text):
    lines = list(filter(None, full_text.split("\n")))
    commands = []
    opening_match = 0
    closing_match = 0
    for line in lines:
        if "!R!" in line:
            opening_match += 1
        elif "EXIT;" in line:
            closing_match += 1
        temp = filter(None, line.replace(";", ";~~").split("~~"))
        for t in temp:
            if temp:
                commands.append(t.strip())

    errors = []

    if "!R!" in lines[0]:
        _temp_msg = ""
        if lines[0].startswith(" "):
            _temp_msg += "Please remove leading whitespace\n"
        if lines[0].endswith(" "):
            _temp_msg += "Please remove trailing whitespace"
        if _temp_msg:
            errors.append(("!R!", _temp_msg))
    else:
        errors.append(("!R!", "!R! missing at beginning of file"))

    if "EXIT;" in lines[-1]:
        _temp_msg = ""
        if lines[-1].startswith(" "):
            _temp_msg += "Please remove leading whitespace\n"
        if lines[-1].endswith(" "):
            _temp_msg += "Please remove trailing whitespace"
        if _temp_msg:
            errors.append(("EXIT;", _temp_msg))
    else:
        errors.append(("EXIT;", "EXIT; missing at end of file"))
        
    if opening_match == 0:
        errors.append(("!R!", "Missing opening command !R!"))
    if closing_match == 0:
        errors.append(("EXIT;", "Missing exit command EXIT;"))
    if opening_match > 1 and opening_match > closing_match:
        errors.append(("!R!", "Too many opening commands"))
    if closing_match > 1 and closing_match > opening_match:
        errors.append(("EXIT;", "Too many closing commands"))

    for command in commands:
        success, reason = parse_command(command)
        if not success:
            errors.append((command, reason))

    return errors


class Parser:
    _instance = None
    _frpo_params_file = "FRPO_parameters.json"
    _kcfg_params_file = "KCFG_parameters.json"
    _prescribe_params_file = "Prescribe_parameters.json"
    _available_commands_file = "available_commands.json"
    _memory = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.kcfg_params = load(cls._kcfg_params_file)
            cls._instance.frpo_syntax = "FRPO" + pparser.Word(pparser.alphanums) + "," + pparser.Word(pparser.alphanums) + ";"
            cls._instance.frpo_params = load(cls._frpo_params_file)
            cls._instance.prescribe_params = load(cls._prescribe_params_file)
            cls._instance.available_commands = load(cls._available_commands_file)
        return cls._instance

    def get_available_commands(self):
        commands = "\n\n"
        for key, val in self.available_commands.items():
            commands += f"{key} - {val.get('Environment')}\n"

        for key, val in self.prescribe_params.items():
            commands += f"{key} - {val.get('Environment')}\n"

        return commands


'''
if __name__ == "__main__":

    tester = Parser()

    idp = load(tester._frpo_independent_params_file)
    dp = load(tester._frpo_dependent_params_file)

    for key, val in idp.items():
        val["Interface"] = "Interface Independent"

    for key, val in dp.items():
        val["Interface"] = "Interface Dependent"

    combined_data = {}
    combined_data.update(idp)
    combined_data.update(dp)
    #for key, val in combined_data.items():
    #    print(key, val)

    with open("FRPO_parameters.json", "w") as f:
        json.dump(combined_data, f, indent=2, sort_keys=True)
        
    pass
'''

