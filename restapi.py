'''
Developed by: Sebastian Peñaherrera
Date: 07/10/2021
Last Updated: 22/04/2024

Description: This is the main file for the REST Server for 360-Video framework. It is responsible for running the REST Server
'''

import uvicorn
from Rest.utils import *
from config_params import ConfigManager
import argparse


if __name__ == "__main__":
    # Create the input ArgumentParser
    parser = argparse.ArgumentParser(description='This is the main file for the REST Server for 360-Video framework.')

    # Add the input parameters
    parser.add_argument('--host', type=str, help='REST host address', default='0.0.0.0')
    parser.add_argument('--port', type=int, help='REST host port', default=8000)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract key-value pair arguments
    ConfigManager.update_parameters("rest_host", args.host)
    ConfigManager.update_parameters("rest_port", args.port)

    # Check if the local_data_path exists, if not create it
    check_local_data_path(ConfigManager.get_parameters('rest_data_path'))

    # Run the rest API app using Uvicorn with the parameters in config_parameters file
    uvicorn.run(app=ConfigManager.get_parameters('rest_app'), port=args.port, host=args.host,
                reload=ConfigManager.get_parameters('rest_reload'))
