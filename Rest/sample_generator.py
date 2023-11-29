import random

from .models import *


class SyntheticSample:
    parameters = {}

    @staticmethod
    def generate_sample(cpe: bool = False):
        sample = {}
        # Get the KQI class field names
        parameters = KQI.__annotations__

        for param in list(parameters.keys()):
            # Parse the data type
            data_type = str(parameters.get(param)).split(" ")[1][1:-2]
            # According to the data type, save a random/default value
            if data_type == 'str':
                sample[param] = "TestValue"
            elif data_type == "int":
                sample[param] = random.randint(1, 10)
            elif data_type == "float":
                sample[param] = random.uniform(1.0, 10.0)
            elif data_type == "bool":
                sample[param] = random.choice([True, False])

        if cpe:
            sample_cpe = {}
            # Get the CPE class field names
            parameters = CPEStats.__annotations__
            for param in list(parameters.keys()):
                cpe_subkey = {}
                # Get the subkey class field names
                sub_parameters = CPEStats.__annotations__[param].__args__[0].__annotations__
                for sub_param in list(sub_parameters.keys()):
                    # Parse the data type
                    data_type = str(sub_parameters.get(sub_param).__args__[0]).split(" ")[1][1:-2]

                    # If the sub_param contains ['sinr', 'rsrp', 'rsrq', 'rssi'] generate int values
                    if contains_partial_string(sub_param, ['sinr', 'rsrp', 'rsrq', 'rssi']):
                        cpe_subkey[sub_param] = random.randint(1, 10)
                    else:
                        # According to the data type, save a random/default value
                        if data_type == 'str':
                            cpe_subkey[sub_param] = "TestValue"
                        elif data_type == "int":
                            cpe_subkey[sub_param] = random.randint(1, 10)
                        elif data_type == "float":
                            cpe_subkey[sub_param] = random.uniform(1.0, 10.0)
                        elif data_type == "bool":
                            cpe_subkey[sub_param] = random.choice([True, False])

                # Append the subkey to the main key
                sample_cpe[param] = cpe_subkey
            # Append the CPE key to the sample
            return {"Service": sample, "CPE": sample_cpe}
        # Return a dictionary of type Service
        return {"Service": sample}


def contains_partial_string(input_string, substrings):
    for substring in substrings:
        if substring in input_string:
            return True
    return False
