import pandas as pd
import json


class ConfigManager:
    # This class provides global variables that are visible by webui, main and callbacks python files
    # Initialize parameters
    parameters = {
        "datVR": {},
        "n_IVR": 0,
        "t_interval": 2000,
        "max_samples": 20,
        "web_app": "webui:app",
        "web_port": 8889,
        "web_host": "0.0.0.0",
        "web_reload": True,
        "web_cpe": False,
        "web_test": False,
        "rest_app": "Rest.rest_server:app",
        "rest_host": "0.0.0.0",
        "rest_port": 8000,
        "rest_reload": True,
        "rest_data_path": "./RestData",
        "rest_n_samples": 20,
    }

    @classmethod
    def update_parameters(cls, key, value):
        if key == "datVR":
            # Convert the dataframe to a dict
            cls.parameters[key] = value.to_dict(orient='index')
        else:
            cls.parameters[key] = value

        cls.write_parameters_json("./config.json")

    @classmethod
    def get_parameters(cls, key):
        cls.read_parameters_json("./config.json")

        if key == "datVR":
            # Return a dataframe
            return pd.DataFrame.from_dict(cls.parameters[key], orient='index')
        else:
            return cls.parameters.get(key, None)

    @classmethod
    def write_parameters_json(cls, path):
        with open(path, 'w') as f:
            json.dump(cls.parameters, f, indent=4)

    @classmethod
    def read_parameters_json(cls, path):
        with open(path, 'r') as f:
            cls.parameters = json.load(f)
