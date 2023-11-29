import json
import time
import os
from datetime import datetime
from config_params import ConfigManager
import re


def get_timestamp():
    # Return the current timestamp
    ts = int(time.time())
    return ts


def get_date():
    # Return the current date
    date = datetime.now().date()
    return date


def get_time():
    # Return the current time
    current_time = datetime.now().time()
    return current_time


def check_dir(path: str):
    # Check if the directory exists
    return os.path.exists(path)


def create_dir(path: str):
    # Create the directory
    if not check_dir(path):
        os.mkdir(path)
        print("The directory {} has been created".format(path))
    else:
        print("The directory {} already exists".format(path))


def check_local_data_path(path: str):
    # Check if the ./data directory exists, else create it
    if not check_dir(path):
        create_dir(path)

    # Check if the ./data_path/date exists, else create it
    date = get_date()
    local_path = get_local_data_path()
    if not check_dir(local_path):
        create_dir(local_path)


def get_local_data_path():
    # Return the path to the ./data_path/date
    return f"{ConfigManager.get_parameters('rest_data_path')}/{get_date()}"


def check_file(path: str):
    # Check if the file exists
    return os.path.exists(path)


def write_file(path: str, content: json, mode: str = 'w'):
    # Check is the directory exists
    check_local_data_path(ConfigManager.get_parameters('rest_data_path'))
    # check_local_data_path(Parameters.rest_data_path)

    # Check if the file already exists
    if check_file(path):
        with open(path, mode=mode) as file:
            json.dump(content, file, indent=4)
    else:
        with open(path, mode='w') as file:
            json.dump(content, file, indent=4)


def convert_dict_to_json(data: dict):
    # Convert the dict to json
    return json.dumps(data, indent=4)


def generate_file_path(timestamp: str, dir_path: str):
    # Save stats in the ./data_path/date/Stats_timestamp.json
    return "{}/Stats_{}.json".format(dir_path, timestamp)


def parse_string_to_int(input_str):
    # If input_str is None, return None
    if input_str is None:
        return input_str

    # If the input is a number, return it
    if isinstance(input_str, int):
        return input_str

    # If the string has special characters, do not parse it
    if not input_str.isalnum():
        return input_str

    # If the string is a hexadecimal number, parse it to int
    if input_str.startswith('0x'):
        return int(input_str, 16)

    # If the string is a hexadecimal number without '0X' at the beginning , parse it to int
    if re.match(r'([A-F]+\d*)', input_str):
        return int(input_str, 16)

    # Use regular expression to extract numeric part
    match = re.match(r'([-+]?\d*\.\d+|\d+)', input_str)
    if match:
        numeric_part = match.group(0)
        return int(float(numeric_part))
    # If parsing fails, raise an exception
    raise ValueError(f"Invalid input: {input_str}")
