from prescribe_lexer import PrescribeLexer, PrescribeStyle
from parser import Parser
import re

def generate_tokens(command):
    parser = Parser()

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

    return tokens

def get_expected_tokens(command):
    parser = Parser()

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

    return tokens

def compare_tokens(expected, given):
    for pos, (expected_token, given_token) in enumerate(zip(expected, given)):
        if expected_token != given_token and expected_token != "?":
            count = 0
            for token in given[:pos]:
                count += len(token)
            return False, f"Expected '{expected_token}' but got '{given_token}' at position {count}"
    return True, "Success"

def main():
    example_command = "FRPO B0,0;"
    tokens = generate_tokens("FRPO B0,0;")
    #print(tokens)
    expected_tokens = get_expected_tokens(tokens)
    #print(expected_tokens)
    print(compare_tokens(expected_tokens, tokens))

    tokens = generate_tokens('KCFG"SCAN"3,2,0;')
    #print(tokens)
    expected_tokens = get_expected_tokens(tokens)
    #print(expected_tokens)
    print('KCFG"SCAN"3,2,0;')
    print(compare_tokens(expected_tokens, tokens))

if __name__ == '__main__':
    main()