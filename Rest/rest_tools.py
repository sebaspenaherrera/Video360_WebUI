# *************************************************************************************************
# Asynchronous REST tools
# Author: Sebastian Peñaherrera
# Date: 07/20/2024
# Summary: This file contains the asynchronous REST tools to send requests to the crowdcell and manage control with the client
# Status: Under development
# *************************************************************************************************

import httpx
from config_params import ConfigManager
import json
from .models import *
from .utils import *

class RestTools:
    
    @staticmethod
    async def configure_http_request(request_type: str = 'GET', host_address: str = '127.0.0.1', port: int | str = 5000, resource: str = '/monitoring', headers: dict = None, query: dict = None, data: dict = None, message: str = None):
        '''
        This async function sends a http request to the specified host_address and port

        Parameters:
        - request_type: str, default='GET'. The type of the request to be sent
        - host_address: str, default='
        - port: int | str, default=5000. The port of the host_address
        - resource: str, default='/monitoring'. The resource to be accessed in the host_address
        - headers: dict, default=None. The headers of the request
        - query: dict, default=None. The query parameters of the request
        - data: dict, default=None. The data to be sent in the request
        - message: str, default=None. The message to be printed to the console

        Returns:
        - A dictionary with the response data and the response status code
        '''
        
        # Check the input parameters
        if isinstance(port, str):
            port = str(ConfigManager.get_parameters(port))
        else:
            port = str(port)
        
        # If host_address contains '.' then it is an IP address
        if '.' in host_address:
            host_address = host_address
        else:
            host_address = ConfigManager.get_parameters(host_address)

        # Configure the header
        base = "http://" + host_address + ":" + port

        if headers is None:
            headers =   {
                        'content-type': 'application/json', 
                        'accept': 'application/json'
                        }

        # Create an httpx request
        async with httpx.AsyncClient() as client:
            log_message(message=f'Sending {request_type} request to {base+resource}', type='INFO')
            if request_type == 'GET':
                response = await client.get(base+resource, headers=headers, params=query)
            elif request_type == 'POST':
                response = await client.post(base+resource, headers=headers, json=data, params=query)
        
        status = response.status_code 
        data_received = response.json()

        # Log the message
        if message is not None:
            if status == 200:
                log_message(f'Succesful request: {message}', type='INFO')
            else:
                log_message(f'Unsuccesful request: {message}', type='ERROR')
        else:
            log_message(f'Request status: {status}', type='DEBUG')

        # Return the response
        return data_received, status
    

    @staticmethod
    async def start_crowd_monitoring(request_type: str ='POST', host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/monitoring', message: str ='Crowd stats monitoring started'):
        '''
        This async function sends a http request to the crowdcell to start the stats monitoring

        Parameters:
        - request_type: str, default='POST'. The type of the request to be sent
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/monitoring'. The resource to be accessed in the crowdcell
        - message: str, default='Crowd stats monitoring started'. The message to be printed to the console

        Returns:
        - A dictionary with the response status code {"Response": 200}
        '''
        
        # Send a http request to the crowdcell to start the stats monitoring
        _, status_code = await RestTools.configure_http_request(request_type=request_type, host_address=host_address, port=port, resource=resource, message= message)

        return {'Response': status_code}
    

    @staticmethod
    async def stop_crowd_monitoring(request_type: str ='GET', host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/monitoring', message: str ='Crowd stats monitoring stopped'):
        '''
        This async function sends a http request to the crowdcell to stop the stats monitoring and fetch the stats

        Parameters:
        - request_type: str, default='GET'. The type of the request to be sent
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/monitoring'. The resource to be accessed in the crowdcell
        - message: str, default='Crowd stats monitoring stopped'. The message to be printed to the console

        Returns:
        - A dictionary with the stats validated by the pydantic model {'Crowdcell_stats': List[CrowdcellSample]{'stat': 'value'}}
        '''

        # Send a http request to the crowdcell to stop the stats monitoring and fetch the stats
        response_data, status_code = await RestTools.configure_http_request(request_type=request_type, host_address=host_address, port=port, resource=resource, message=message)

        # Validate the response to fit the pydantic model
        data = {'Crowdcell_stats' : response_data}
        data = CrowdcellStats.model_validate(data).model_dump()
        
        return data


    @staticmethod
    async def start_crowd_cpu_monitoring(request_type: str ='POST', host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/resources/monitor/', message: str = 'Crowd CPU monitoring started', body: dict = None):
        '''
        This async function sends a http request to the crowdcell to start the CPU monitoring

        Parameters:
        - request_type: str, default='POST'. The type of the request to be sent
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/resources/monitor/'. The resource to be accessed in the crowdcell
        - message: str, default='Crowd CPU monitoring started'. The message to be printed to the console

        Returns:
        - A dictionary with the response status code {"Response": 200}
        '''
        
        # Send a http request to the crowdcell to start the CPU monitoring
        body = {
                "type": "process",
                "process": "lteenb-avx2"
                }
        
        _, status_code = await RestTools.configure_http_request(request_type=request_type, host_address=host_address, port=port, resource=resource, data=body, message=message)

        return {'Response': status_code}


    @staticmethod
    async def stop_crowd_cpu_monitoring(request_type: str ='GET', host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/resources/monitor/', message: str ='Crowd CPU monitoring stopped'):
        '''
        This async function sends a http request to the crowdcell to stop the CPU monitoring

        Parameters:
        - request_type: str, default='GET'. The type of the request to be sent
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/resources/monitor/'. The resource to be accessed in the crowdcell
        - message: str, default='Crowd CPU monitoring stopped'. The message to be printed to the console

        Returns:
        - A dictionary with the CPU stats validated by the pydantic model {'CPU_stats': List[CPUSample]{'stat': 'value'}}
        '''
        
        # Send a http request to the crowdcell to stop the CPU monitoring
        response_data, status_code = await RestTools.configure_http_request(request_type=request_type, host_address=host_address, port=port, resource=resource, message=message)

        # Validate the response to fit the pydantic model
        data = {'CPU_stats' : response_data}
        data = CPUMonitoring.model_validate(data).model_dump()

        return data
    

    @staticmethod
    async def monitor_crowd():
        '''
        This async function starts the crowd monitoring and the CPU monitoring

        Returns:
        - A dictionary with the response status code {"Response": "OK"} if the monitoring started successfully
        '''

        # Start the crowd stats monitoring. If it fails, return a ''failed'' response
        crowd_response = await RestTools.start_crowd_monitoring(request_type='POST', host_address='rest_crowd_host', port='rest_crowd_port', resource='/monitoring', message='Crowd stats monitoring started')

        if crowd_response.get('Response') == 200:
            log_message(message='Crowd monitoring started', type='DEBUG')


            # Start the CPU monitoring
            crowd_response = await RestTools.start_crowd_cpu_monitoring(request_type='POST', host_address='rest_crowd_host', port='rest_crowd_port', resource='/resources/monitor/', message='Crowd CPU monitoring started')

            if crowd_response.get('Response') == 200:
                log_message(message='Crowd CPU monitoring started', type='DEBUG')
                response = {'Response': 'OK'}
            else:
                log_message(message='Crowd CPU monitoring failed', type='ERROR')
                response = {'Response': 'Failed'}
            
            response['Status'] = True
        else:
            log_message(message='Crowd monitoring failed', type='ERROR')
            response = {'Response': 'Failed', 'Status': False}

        return response
    

    @staticmethod
    async def terminate_monitoring_crowd():
        '''
        This async function stops the crowd monitoring and the CPU monitoring. It also fetches the stats throughout the monitoring period

        Returns:
        - A dictionary with the response status code {"Response": "OK"} if the monitoring stopped successfully and the stats have been fetched
        '''

        # Stop the crowd stats monitoring. If it fails, return a ''failed'' response
        crowd_stats = await RestTools.stop_crowd_monitoring(request_type='GET', host_address='rest_crowd_host', port='rest_crowd_port', resource='/monitoring', message='Crowd stats monitoring stopped')

        if crowd_stats.get('Crowdcell_stats') is not None:
            log_message(message='Crowd monitoring stopped. Stats have been fetched', type='DEBUG')

            # Stop the CPU monitoring
            cpu_stats = await RestTools.stop_crowd_cpu_monitoring(request_type='GET', host_address='rest_crowd_host', port='rest_crowd_port', resource='/resources/monitor/', message='Crowd CPU monitoring stopped')

            if cpu_stats.get('CPU_stats') is not None:
                log_message(message='Crowd CPU monitoring stopped', type='DEBUG')
                response = {'Response': 'OK'}
            else:
                log_message(message='Crowd CPU monitoring failed', type='ERROR')
                response = {'Response': 'Failed'}
            
            response['Status'] = True
        else:
            log_message(message='Crowd monitoring failed', type='ERROR')
            response = {'Response': 'Failed', 'Status': False}

        # Add the stats to the response
        response.update(crowd_stats)
        response.update(cpu_stats)

        return response
    

    @staticmethod
    async def set_gain(gain: int, host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/amarisoft/enb/cell_gain', message: str ='Gain set'):
        '''
        Set the gain of the crowdcell. Values between 0 and -100 dB

        Parameters:
        - gain: int. The gain value to be set
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/amarisoft/enb/cell_gain'. The resource to be accessed in the crowdcell
        - message: str, default='Gain set'. The message to be printed to the console

        Returns:
        - None
        '''
        
        # Set the body of the request
        body = {
                'cell_id' : 1,
                "gain": gain
                }
        
        # Send a http request to the crowdcell to set the gain
        _, status_code = await RestTools.configure_http_request(request_type='POST', host_address=host_address, port=port, resource=resource, message= message, data=body)

        if status_code == 200:
            log_message(f'Succesfully {message} to {gain}', type='DEBUG')
        else:
            log_message(f'Failed to {message} to {gain}', type='ERROR')

        return {'Response': status_code}
    

    @staticmethod
    async def set_noise_level(noise_level: int, host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/amarisoft/enb/noise_level', message: str ='Noise level set'):
        '''
        Set the noise level of the crowdcell. Values between -30 and 0 dB

        Parameters:
        - noise_level: int. The noise level value to be set
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/amarisoft/enb/cell_noise'. The resource to be accessed in the crowdcell
        - message: str, default='Noise level set'. The message to be printed to the console

        Returns:
        - None
        '''

        # Set the body of the request
        body = {
                'cell_id' : 1,
                "noise_level": noise_level
                }
        
        # Send a http request to the crowdcell to set the noise level
        _, status_code = await RestTools.configure_http_request(request_type='POST', host_address=host_address, port=port, resource=resource, message= message, data=body)

        if status_code == 200:
            log_message(f'Succesfully {message} to {noise_level}', type='DEBUG')
        else:
            log_message(f'Failed to {message} to {noise_level}', type='ERROR')

        return {'Response': status_code}
    

    @staticmethod
    async def set_prbs(prbs: int, rb_start: int = 0, cell_id: int = 1, host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/amarisoft/enb/config_set', message: str ='Allocated PRBs set'):
        '''
        Set the PRBs of the crowdcell

        Parameters:
        - prbs: int. The PRBs value to be set
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/amarisoft/enb/config_set'. The resource to be accessed in the crowdcell
        - message: str, default='Allocated PRBs set'. The message to be printed to the console

        Returns:
        - None
        '''

        # Set the body of the request
        body = {
                "cells":{
                    str(cell_id):{
                        
                        "pdsch_fixed_rb_alloc": True,
                        "pdsch_fixed_rb_start": rb_start,
                        "pdsch_fixed_l_crb":  prbs
                    }
                    } 
                }
        
        # Send a http request to the crowdcell to set the PRBs
        _, status_code = await RestTools.configure_http_request(request_type='POST', host_address=host_address, port=port, resource=resource, message= message, data=body)

        if status_code == 200:
            log_message(f'Succesfully {message} to {prbs}', type='DEBUG')
        else:
            log_message(f'Failed to {message} to {prbs}', type='ERROR')

        return {'Response': status_code}
    

    @staticmethod
    async def set_mcs(mcs: int, cell_id: int = 1, host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/amarisoft/enb/config_set', message: str ='MCS value set'):
        '''
        
        '''

        # Set the body of the request
        body = {
                "cells":{
                    str(cell_id):{
                                "pdsch_mcs": mcs
                                }
                    } 
                }
        
        # Send a http request to the crowdcell to set the PRBs
        _, status_code = await RestTools.configure_http_request(request_type='POST', host_address=host_address, port=port, resource=resource, message= message, data=body)

        if status_code == 200:
            log_message(f'Succesfully {message} to {mcs}', type='DEBUG')
        else:
            log_message(f'Failed to {message} to {mcs}', type='ERROR')

        return {'Response': status_code}
    

    @staticmethod
    async def reset_crowdcell(host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/crowdcell/restartService', message: str ='Crowdcell reset'):
        '''
        Reset the crowdcell

        Parameters:
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/amarisoft/enb/reset'. The resource to be accessed in the crowdcell
        - message: str, default='Crowdcell reset'. The message to be printed to the console

        Returns:
        - None
        '''

        # Send a http request to the crowdcell to reset it
        _, status_code = await RestTools.configure_http_request(request_type='POST', host_address=host_address, port=port, resource=resource, message= message)

        if status_code == 200:
            log_message(f'Succesfully {message}', type='DEBUG')
        else:
            log_message(f'Failed to {message}', type='ERROR')

        return {'Response': status_code}
    

    @staticmethod
    async def get_crowdcell_configuration_file(host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/configuration/all', message: str ='Crowdcell configuration file fetched'):
        '''
        Get the crowdcell configuration file

        Parameters:
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/amarisoft/enb/config'. The resource to be accessed in the crowdcell
        - message: str, default='Crowdcell configuration file fetched'. The message to be printed to the console

        Returns:
        - A dictionary with the configuration file
        '''

        # Send a http request to the crowdcell to get the configuration file
        response_data, status_code = await RestTools.configure_http_request(request_type='GET', host_address=host_address, port=port, resource=resource, message= message)

        if status_code == 200:
            log_message(f'Succesfully {message}', type='DEBUG')
        else:
            log_message(f'Failed to {message}', type='ERROR')

        return response_data
    

    @staticmethod
    async def get_crowdcell_enb_configuration(host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/amarisoft/enb/config_get', message: str ='Crowdcell eNB configuration fetched'):
        '''
        Get the crowdcell configuration

        Parameters:
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/amarisoft/enb/config'. The resource to be accessed in the crowdcell
        - message: str, default='Crowdcell configuration fetched'. The message to be printed to the console

        Returns:
        - A dictionary with the configuration
        '''

        # Send a http request to the crowdcell to get the configuration
        response_data, status_code = await RestTools.configure_http_request(request_type='POST', host_address=host_address, port=port, resource=resource, message= message)

        if status_code == 200:
            log_message(f'Succesfully {message}', type='DEBUG')
        else:
            log_message(f'Failed to {message}', type='ERROR')

        return response_data
    

    @staticmethod
    async def reset_crowdcell_log(host_address: str ='rest_crowd_host', port: int | str ='rest_crowd_port', resource: str ='/amarisoft/enb/log_reset', message: str ='Crowdcell log reset'):
        '''
        Reset the crowdcell log

        Parameters:
        - host_address: str, default='rest_crowd_host'. The address of the crowdcell
        - port: int | str, default='rest_crowd_port'. The port of the crowdcell
        - resource: str, default='/amarisoft/enb/reset'. The resource to be accessed in the crowdcell
        - message: str, default='Crowdcell log reset'. The message to be printed to the console

        Returns:
        - None
        '''

        # Send a http request to the crowdcell to reset the log
        _, status_code = await RestTools.configure_http_request(request_type='POST', host_address=host_address, port=port, resource=resource, message= message)

        if status_code == 200:
            log_message(f'Succesfully {message}', type='DEBUG')
        else:
            log_message(f'Failed to {message}', type='ERROR')

        return {'Response': status_code}    