'''
Developer: Sebastian Peñaherrera
Date: 07/10/2021
Last Updated: 22/04/2024
Version: 2.0

Description: This is the main file for the WebUI for 360-Video framework. It is responsible for running the WebUI
'''

import uvicorn
import argparse
from config_params import ConfigManager


if __name__ == "__main__":
    # Create the input ArgumentParser
    parser = argparse.ArgumentParser(description='This is the main file for the WebUI for 360-Video framework.')

    # Add the input parameters
    parser.add_argument('--host', type=str, help='WebUI host address', default='0.0.0.0')
    parser.add_argument('--port', type=int, help='WebUI host port', default=8889)
    parser.add_argument('--cpe', type=str, help='Enables/Disables CPE metrics', default=False)
    parser.add_argument('--test', type=str, help='Enables/Disables test synthetic samples module', default=False)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract key-value pair arguments
    port = args.port
    host = args.host
    cpe = args.cpe in ['true', '1', 't', 'y', 'yes', 'yeah', 'True', 'certainly', 'uh-huh']
    test = args.test in ['true', '1', 't', 'y', 'yes', 'yeah', 'True', 'certainly', 'uh-huh']

    # Update the configuration json file with the input parameters
    ConfigManager.update_parameters("web_host", host)
    ConfigManager.update_parameters("web_port", port)
    ConfigManager.update_parameters("web_cpe", cpe)
    ConfigManager.update_parameters("web_test", test)

    print(f"{ConfigManager.get_parameters('web_cpe')} AND {ConfigManager.get_parameters('web_test')}")

    # Run the rest API app using Uvicorn with the parameters in config_parameters file
    uvicorn.run(app=ConfigManager.get_parameters('web_app'), port=port, host=host,
                reload=ConfigManager.get_parameters('web_reload'))
