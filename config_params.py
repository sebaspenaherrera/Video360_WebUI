import pandas as pd
import json


def check_config_file():
    '''
    Define the default parameters of the config.json file. If the file does not exist, create it with the default parameters

    Parameters:
    - None

    Returns:
    - The default parameters of the config.json file
    '''
    
    # Set the default parameters
    params = {
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
        "rest_crowd_host": "192.168.159.160",
        "rest_crowd_port": 5000
    }

    # Check if the config.json file exists, else create it
    try:
        with open("./config.json", 'r') as f:
            params = json.load(f)
    except FileNotFoundError:
        with open("./config.json", 'w') as f:
            json.dump(params, f, indent=4)

    # Return the parameters
    return params


class ConfigManager:
    '''
    This class provides global variables that are visible by webui, main and callbacks python files
    '''

    # Initialize parameters
    parameters = {}

    # Check if the config.json file exists, else create it
    parameters = check_config_file()


    @classmethod
    def update_parameters(cls, key, value):
        '''
        Update the parameters of the config.json file. It does not require object instantiation but uses class attributes

        Parameters:
        key: str. The key of the parameter to be updated
        value: any. The value of the parameter to be updated

        Returns:
        - None
        '''
        
        if key == "datVR":
            # Convert the dataframe to a dict
            cls.parameters[key] = value.to_dict(orient='index')
        else:
            cls.parameters[key] = value

        cls.write_parameters_json("./config.json")


    @classmethod
    def get_parameters(cls, key):
        '''
        Get the parameter defined by the key in the config.json file. It does not require object instantiation but uses class attributes

        Parameters:
        key: str. The key of the parameter to be retrieved

        Returns:
        - The value of the parameter
        '''
        
        cls.read_parameters_json("./config.json")

        if key == "datVR":
            # Return a dataframe
            return pd.DataFrame.from_dict(cls.parameters[key], orient='index')
        else:
            return cls.parameters.get(key, None)


    @classmethod
    def write_parameters_json(cls, path):
        '''
        Write the config.json file. It does not require object instantiation but uses class attributes

        Parameters:
        path: str. The path to the config.json file

        Returns:
        - None
        '''
        
        with open(path, 'w') as f:
            json.dump(cls.parameters, f, indent=4)


    @classmethod
    def read_parameters_json(cls, path):
        '''
        Read the config.json file. Then saves the parameters in the class attribute. It does not require object instantiation but uses class attributes

        Parameters:
        path: str. The path to the config.json file

        Returns:
        - None
        '''
        
        with open(path, 'r') as f:
            cls.parameters = json.load(f)

