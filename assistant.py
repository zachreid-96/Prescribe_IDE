import os, json, time, faiss
from llama_cpp import Llama, LlamaGrammar
from sentence_transformers import SentenceTransformer

## Public Methods
# generate_faiss_index_metadata
# get_result
# Class Assistant

def _load(f):
    if os.path.exists(f):
        with open(f, "r") as params:
            data = json.load(params)
        return data
    return None

def _format_text(key, val):
    _formatted_text = ""

    if val.get('Values', []):
        _formatted_text = (f"Command {key} adjusts the {val.get('Environment', '')}."
                           f" The defaulted factory setting value is {val.get('Factory Setting', '')}.")
        if val.get('Multi-Parameter', 0) == 0:
            _formatted_text += f" The command accepts an {val.get('Values', '')[0].get('Type', '')} value representing an {val.get('Values', '')[0].get('Comment', '')} in Position #1."
            _formatted_text += f" The command format is {val.get('Format', '')}."
        else:
            _last_pos = 0
            for inx, opt in enumerate(val.get('Values', '')):
                if _last_pos == opt.get('Position', 0):
                    continue
                _last_pos = opt.get('Position')
                _formatted_text += f" The command accepts an {opt.get('Type', '')} value representing an {opt.get('Comment', '')} in Position #{_last_pos}."
            _formatted_text += f" The command format is {val.get('Format', '')}."
    else:
        _formatted_text = (f"Command {key} gets the {val.get('Environment', '')}."
                           f" The defaulted factory setting value is {val.get('Factory Setting', '')}."
                           f" The command does not accept any parameters."
                           f" The command format is {val.get('Format', '')}.")

    return _formatted_text

def _handle_single_parameter(text_desc, values):
    for arg in values:
        if arg.get('Type', '') == "Enum":
            for _arg_key, _arg_val in arg.get('Options', []).items():
                text_desc += f"{_arg_key} = {_arg_val}\n"
        elif arg.get('Type', '') == "Range":
            text_desc += f"Min Value = {arg.get('min', '')} and Max value = {arg.get('max', '')}\n"
        elif arg.get('Type', '') == "Integer":
            text_desc += f"Takes an Integer value representing {arg.get('Comment', '')}\n"
        elif arg.get('Type', '') == "String":
            text_desc += f"Takes an String value representing {arg.get('Comment', '')}\n"

    return text_desc

def _handle_multi_parameter(text_desc, values):
    _last_pos = 0
    for arg in values:
        if _last_pos != arg.get('Position', 0):
            _last_pos = arg.get('Position', 0)
            text_desc += f"The command accepts the following arguments in Position #{_last_pos}: \n"
        if arg.get('Type', '') == "Enum":
            for _arg_key, _arg_val in arg.get('Options', []).items():
                text_desc += f"{_arg_key} = {_arg_val}\n"
        elif arg.get('Type', '') == "Range":
            text_desc += f"Min Value = {arg.get('min', '')} and Max value = {arg.get('max', '')}\n"
        elif arg.get('Type', '') == "Integer":
            text_desc += f"Takes an Integer value representing {arg.get('Comment', '')}\n"
        elif arg.get('Type', '') == "String":
            text_desc += f"Takes an String value representing {arg.get('Comment', '')}\n"

    return text_desc

def _handle_conditional_parameter(text_desc, values):
    _position = 0
    _parent_option = 0
    _parent_position = 0
    _grandparent_option = 0
    for arg in values:
        _position = arg.get('Position', 0)
        _parent_option = arg.get('Parent Option', 0)
        _parent_position = arg.get('Parent Position', 0)
        _grandparent_option = arg.get('Grandparent Option', 0)

        if _parent_position == 0 and _grandparent_option == 0:
            text_desc += f"The command accepts the following arguments in Position #{_position}: \n"
        elif _parent_position > 0 and _grandparent_option == 0:
            text_desc += f"The command accepts the following arguments in Position #{_position} WITH Parent Position #{_parent_position} AND Parent Option = {_parent_option}\n"
        elif _parent_position > 0 and _grandparent_option > 0:
            text_desc += f"The command accepts the following arguments in Position #{_position} WITH Parent Position #{_parent_position} AND Parent Option = {_parent_option} AND Grandparent Option = {_grandparent_option}\n"

        if arg.get('Type', '') == "Enum":
            for _arg_key, _arg_val in arg.get('Options', []).items():
                text_desc += f"{_arg_key} = {_arg_val}\n"
        elif arg.get('Type', '') == "Range":
            text_desc += f"Min Value = {arg.get('min', '')} and Max value = {arg.get('max', '')}\n"
        elif arg.get('Type', '') == "Integer":
            text_desc += f"Takes an Integer value representing {arg.get('Comment', '')}\n"
        elif arg.get('Type', '') == "String":
            text_desc += f"Takes an String value representing {arg.get('Comment', '')}\n"

    return text_desc

def _format_entries():

    _text_entries = {}

    for json_file in [r"json/KCFG_parameters.json", r"json/FRPO_parameters.json", r"json/Prescribe_parameters.json"]:
        json_data = _load(json_file)
        for _key, _val in json_data.items():
            _text_desc = (f"Name: {_val.get('Environment', '')}\n"
                          f"Format: {_val.get('Format', '')}\n"
                          f"Parameter: {_val.get('Parameter', '')}\n")
            _values = _val.get('Values', [])
            if _values:
                if _val.get('Multi-Parameter', 0) == 0:
                    _text_desc += "The command accepts the following arguments in Position #1: \n"
                    _text_desc = _handle_single_parameter(_text_desc, _values)
                elif _val.get('Multi-Parameter', 0) == 1 and _val.get('Conditional', 0) == 0:
                    _text_desc = _handle_multi_parameter(_text_desc, _values)
                elif _val.get('Conditional', 0) == 1:
                    _text_desc = _handle_conditional_parameter(_text_desc, _values)
            else:
                _text_desc += f"This parameter does not take any arguments. But it does {_val.get('Note', '')}\n"

            _text_entries[_key] = _text_desc

    return _text_entries

def generate_faiss_index_metadata():
    _model = SentenceTransformer('all-MiniLM-L6-v2')

    _formatted_entries = _format_entries()

    _metadata_extra_data = {}
    _metadata_bank = {}
    for json_file in [r"json/KCFG_parameters.json", r"json/FRPO_parameters.json", r"json/Prescribe_parameters.json"]:
        json_data = _load(json_file)
        for _key, _val in json_data.items():
            _text_desc = _format_text(_key, _val)
            _metadata_bank[_key] = _formatted_entries[_key]
            _metadata_extra_data[_key] = _val

    _keys = list(_metadata_bank.keys())
    _values = list(_metadata_bank.values())

    _embeddings = _model.encode(_values, normalize_embeddings=True)

    _dimensions = _embeddings.shape[1]
    _faiss_index = faiss.IndexFlatIP(_dimensions)
    _faiss_index.add(_embeddings)

    _metadata_format = {}
    for _key, _val in _metadata_bank.items():
        #print(_metadata_extra_data[_key])
        _metadata_format[_key] = {
            "Prescribe Command": f"{_key}",
            "Text Description": f"{_val}",
            "Original Entry": _metadata_extra_data[_key],
            "Format": f"{_metadata_extra_data[_key].get('Format', '')}"
        }

    faiss.write_index(_faiss_index, r"faiss/Prescribe_Index.faiss")
    json.dump(_metadata_format, open(r"json/Prescribe_Index_Metadata.json", "w"), indent=2)

def _load_faiss_index():

    if os.path.exists(r"faiss/Prescribe_Index.faiss"):
        _index = faiss.read_index(r"faiss/Prescribe_Index.faiss")
        return _index
    return None

def _load_metadata():

    if os.path.exists(r"json/Prescribe_Index_Metadata.json"):
        _metadata = _load(r"json/Prescribe_Index_Metadata.json")
        return _metadata
    return None

def _load_model():

    if os.path.exists(r"models/Phi-3-mini-4k-instruct-q4.gguf"):
        _cpu_count = max(1, os.cpu_count() // 2)
        _llm = Llama(model_path=r"./models/Phi-3-mini-4k-instruct-q4.gguf", n_ctx=4096, n_threads=_cpu_count,
                    verbose=False)
        return _llm
    return None

def _get_nearest_indices(user_request):

    _assistant = Assistant()

    _faiss_model = _assistant.faiss_index
    _metadata = _assistant.metadata

    _model = SentenceTransformer('all-MiniLM-L6-v2')

    _query_vector = _model.encode([user_request])
    k = 1
    _, indic = _faiss_model.search(_query_vector, k)

    _keys = list(_metadata.keys())

    _nearest_neighbors = ""
    _nearest_neighbor_formats = []
    _nearest_neighbor_options = []

    #'''
    for i, index in enumerate(indic[0]):
        #print(type(_metadata[_keys[index]].get('Original Entry')))
        _nearest_neighbors += f"{_metadata[_keys[index]].get('Text Description', '')}\n"
        _nearest_neighbor_formats.append(_metadata[_keys[index]].get('Format', ''))
        _nearest_neighbor_options.append(_metadata[_keys[index]].get('Original Entry', '').get('Values', []))
    #'''
    _nearest_neighbors += "\n"

    return _nearest_neighbors, _nearest_neighbor_formats, _nearest_neighbor_options

def _format_grammar_options(options):

    _options = []
    for i, opt in enumerate(filter(None, options)):
        _last_pos_seen = 0
        _temp_str = ""
        for val in opt:
            if val.get('Position') != _last_pos_seen:
                _temp_str = f"arg{i+1} ::= "
                _last_pos_seen = val.get('Position')

                if val.get('Type') == "Enum":
                    _opt = list(filter(None, val.get('Options').keys()))
                    _temp_str += " | ".join(f'"{str(v)}"' for v in _opt)
                    _options.append(_temp_str)
                if val.get('Type') == "Range":
                    _opt = list(range(int(val.get('min')), int(val.get('max')) + 1))
                    _temp_str += " | ".join(f'"{str(v)}"' for v in _opt)
                    _options.append(_temp_str)

            elif val.get('Position') == _last_pos_seen:
                if val.get('Type') == "Enum":
                    _opt = list(filter(None, val.get('Options').keys()))
                    _temp_str += " | ".join(f'"{str(v)}"' for v in _opt)
                    _options[i] += " | " + " | ".join(f'"{str(v)}"' for v in _opt)
                if val.get('Type') == "Range":
                    _opt = list(range(int(val.get('min')), int(val.get('max')) + 1))
                    _temp_str += " | ".join(f'"{str(v)}"' for v in _opt)
                    _options[i] += " | " + " | ".join(f'"{str(v)}"' for v in _opt)

    return "\n".join(_options)

def _format_grammar_formats(formats):
    # Print Event Log; Turn on Three Tier Color Monitoring; Increase RAM to 128MB
    _formats = []
    _temp = None
    _arg_counter = 1
    for i, form in enumerate(formats):
        form.replace(';', '')
        _temp = list(filter(None, form.split(',')))
        if 'STAT' in form:
            _temp = ['STAT', '#1']

        if not _temp:
            return []

        _root_format = _temp[0]
        _temp_form = ""

        if len(_temp) > 1:
            if '"' in _root_format:
                _t = list(filter(None, _root_format.split('"')))
                _temp_form += fr'line{i + 1} ::= "{_t[0]}\"{_t[1]}\"," '
            elif 'STAT' in _root_format:
                _temp_form += f'line{i + 1} ::= "{_root_format} " '
            else:
                _temp_form += f'line{i+1} ::= "{_root_format}, " '
        else:
            if '"' in _root_format:
                _t = list(filter(None, _root_format.split('"')))
                _temp_form += fr'line{i + 1} ::= "{_t[0]}\"{_t[1]}\"" '
            else:
                _temp_form += f'line{i + 1} ::= "{_root_format}" '

        _temp_args = []
        for _ in _temp[1:]:
            _temp_args.append(f"arg{_arg_counter}")
            _arg_counter += 1
        if 'STAT' in _temp_form:
            _temp_form += r" ".join(_temp_args)
        else:
            _temp_form += r" , ".join(_temp_args)

        _temp_form += r' ";"'
        _formats.append(_temp_form)

    return "\n".join(_formats)

def _run_model(tokens, gram, user_request):

    _assistant = Assistant()

    _return_msg = ""
    if _assistant.faiss_index is None:
        _return_msg += "Unable to load FAISS Index\n"
    if _assistant.metadata is None:
        _return_msg += "Unable to load metadata\n"
    if _assistant.model is None:
        _return_msg += "Unable to load model\n"

    if _return_msg != "":
        return _return_msg

    llm = _assistant.model

    header = (
        "You generate Valid Kyocera PRESCRIBE PDL commands.\n"
        "Do NOT invent values. Use ONLY values found in Given Data.\n\n"
        "Output Contract:\n"
        f"- Return exactly {len(user_request)} lines: one PRESCRIBE command per line, same order.\n"
        "- No headers, no reasoning, no labels, no blank lines, no extra lines.\n"
        "- Each line MUST end with ';'.\n"
        "- Replace ONLY the placeholders (#1, #2, #3) with correct values. Do not alter the parameters.\n"
        "- Use the values provided for each command. Do NOT leave placeholders like #1 or #2.\n"
        "- Do NOT output the parameter. Do NOT output the reasoning.\n"
        "- Do NOT output Instructions. Do NOT output Explanation.\n"
        "Given Data (authoritative; per line):\n"
    )

    blocks = []
    for i, (text_desc, req) in enumerate(zip(tokens, user_request), start=1):
        blocks.append(f"[{i}] {req}\n{text_desc.strip()}\n")

    # Single sentinel to stop generation
    sentinel = " << < END >> > "

    prompt = header + "\n".join(blocks) + sentinel

    grammar = LlamaGrammar.from_string(gram)

    response = llm(
        prompt=prompt,
        max_tokens=128,
        temperature=0.0,
        top_p=1.0,
        top_k=1,
        repeat_penalty=1.05,
        seed=42,
        grammar=grammar,
        stop=["<<<<END>>>>", "Instructions:", "Explanation:", "Reasoning:", "Format:"],
        echo=False
    )
    return response['choices'][0]['text']


def _process_user_request(user_input):
    _tokens = []
    _formats = []
    _options = []
    _user_request_commands = list(filter(None, user_input.split(';')))
    if len(_user_request_commands) == 1:
        _tokens, _formats, _options = _get_nearest_indices(_user_request_commands[0])
    elif len(_user_request_commands) > 1:
        for request_command in _user_request_commands:
            _token, _format, _option = _get_nearest_indices(request_command)
            _tokens.append(_token)
            _formats.extend(_format)
            _options.extend(_option)


    _formats = _format_grammar_formats(_formats)
    _options = _format_grammar_options(_options)

    _root = "root ::= " + r' "\n" '.join(f"line{v}" for v in range(1, len(_formats.split('\n')) + 1))
    _grammar = (f"{_root}" + "\n"
                f"{_formats}" + "\n"
                f"{_options}")

    return _tokens, _grammar, _user_request_commands


def get_result(user_request):

    _tokens, _grammar, _user_request_commands = _process_user_request(user_request)
    #print("Grammar\n", _grammar)
    _result = _run_model(_tokens, _grammar, _user_request_commands)
    #print("Output:" + "\n" + _result)
    _commands = list(filter(None, _result.split('\n')))
    _filtered_commands = [command for command in _commands
                          if ';' in command]

    return _filtered_commands

class Assistant:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.faiss_index = _load_faiss_index()
            cls._instance.metadata = _metadata = _load_metadata()
            cls._instance.model = _load_model()

        return cls._instance

'''
if __name__ == "__main__":
    #generate_faiss_index_metadata()
    _load_start = time.time()
    _assistant = Assistant()
    _load_end = time.time()
    print(f"loaded faiss/model in {_load_end - _load_start:.4f} seconds")

    _user_request = input("Enter Command: ")

    _model_start = time.time()
    _result = get_result(_user_request)
    _model_end = time.time()
    #print(_result)
    print(f"ran model in {_model_end - _model_start:.4f} seconds")

    #print(_result)
    
#'''