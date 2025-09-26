import os.path
import json
import pyparsing as pparser


def load(f):
    if os.path.exists(f):
        with open(f, "r") as params:
            data = json.load(params)
        return data


class Parser:
    _instance = None
    _frpo_independent_params_file = "Interface-independent-parameters.json"
    _frpo_dependent_params_file = "Interface-dependent-parameters.json"
    _kcfg_params_file = "Kyocera-configuration-parameters.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.independent_params = load(cls._frpo_independent_params_file)
            cls._instance.dependent_params = load(cls._frpo_dependent_params_file)
            cls._instance.kcfg_params = load(cls._kcfg_params_file)
            cls._instance.frpo_syntax = "FRPO" + pparser.Word(pparser.alphanums) + "," + pparser.Word(pparser.alphanums) + ";"
            cls._instance.frpo_params = cls.load_frpo()
        return cls._instance

    def load_frpo(self):
        if os.path.exists(self._frpo_independent_params_file):
            with open(self._frpo_independent_params_file, "r") as params:
                data = json.load(params)
            return data

if __name__ == "__main__":

    pass


