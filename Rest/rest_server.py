#**********************************************************************
# REST API server for testbed monitoring and crowdcell monitoring
# Author: Sebastian Peñaherrera
# Created: 2021-07-01 00:05:00
# Status: Under development (v2.X)
#**********************************************************************

from fastapi import FastAPI, Query, Path, Body
from typing import Annotated
from .models import *
from .Stats import Stats
from .utils import *
from .sample_generator import SyntheticSample as Synthetic
from config_params import ConfigManager
import httpx
from .rest_tools import RestTools as tools
from starlette.responses import RedirectResponse

stats = Stats(n_samples=ConfigManager.get_parameters('rest_n_samples'))
app = FastAPI()


# ***************************************************** REST API ENDPOINTS ************************************************************

# DEFAULT ENDPOINT ***************************************************************
@app.get("/", tags=["Default"])
async def redirect_docs():
    # Redirect to the documentation page
    return RedirectResponse(url="/docs/")


# VIDEO360-RELATED ENDPOINTS ****************************************************

@app.get("/service/video360/demo", tags=["Video360"])
async def get_samples(n_items: Annotated[int, Query(le=ConfigManager.get_parameters('rest_n_samples'))] = 1,
                      cpe: Annotated[bool, Query()] = False):
    '''
    This endpoint returns a number of samples from the stats buffer

    Parameters:
    - n_items: int, default=1. The number of samples to be returned
    - cpe: bool, default=False. If True, returns the CPE data

    Returns:
    - A dictionary with the samples data
    '''
    
    # If the number of items is equal or less than n_samples, get n_samples from stats buffer
    data = stats.get_items(end=n_items, cpe=cpe)

    # TODO: Implement the crowd monitoring stats in real-time
    return data


@app.get("/service/video360/generate_sample", tags=["Video360"])
async def get_synthetic_sample(cpe: Annotated[bool, Query()] = False):
    '''
    This endpoint generates a synthetic sample with random value using the KQI model format

    Parameters:
    - cpe: bool, default=False. If True, returns the CPE data

    Returns:
    - A dictionary with the synthetic sample data
    '''
    
    # Create a fake sample using KQI model format
    data = Synthetic.generate_sample(cpe=cpe)
    return data


@app.post("/service/video360/testbed/{timestamp}", tags=["Video360"])
async def save_session(timestamp: Annotated[int, Path(ge=0)],
                       data: Annotated[SessionStats | None, Body(examples=[example_POST_testbed])]):
    '''
    This endpoint saves the session stats data (a 360-video session) in a JSON file

    Parameters:
    - timestamp: int. The timestamp of the session
    - data: SessionStats. The session stats data

    Returns:
    - A dictionary with the timestamp and a confirmation message
    '''

    # HARDCODE: Request crowdcell to send the stats measured during the session
    if stats.get_crowd_invoked():
        crowd_stats = await tools.terminate_monitoring_crowd() 
    else:
        log_message(message="Crowdcell monitoring not invoked", type='WARNING')

    # Parse body data as dict-base json
    data_json = data.model_dump()
    log_message(message=f"Service client stats: {data_json}", type='INFO')

    # HARDCODE: Append the crowdcell stats to the session data
    if stats.get_crowd_invoked():
        data_json.update(crowd_stats)

    # Write and save as a JSON file in the data folder
    path_file = generate_file_path(str(timestamp), get_local_data_path())
    write_file(path_file, content=data_json, mode='w')
    
    log_message(message=f"Session stats saved in {path_file}. Enabling next experiment...", type='SUCCESS', bold=True)

    # Return a confirmation message
    return {"timestamp": timestamp, "message": "Session stats received"}


@app.post("/service/video360/demo/", tags=["Video360"])
async def append_sample(data: Annotated[SampleStats | None, Body(examples=[example_POST_demo])] = None):
    '''
    This endpoint receives a sample and appends it to the stats buffer. Used for demo purposes

    Parameters:
    - data: SampleStats. The sample data following the KQI pydantic model (SampleStats)

    Returns:
    - A dictionary with the timestamp and a confirmation message
    '''

    # Append dictionary to the list of samples
    if stats is not None:
        # Parse "CPE" fields that contains "MHz" and "dBm" units to float
        data = data.model_dump()

        # If data contains a 'CPE' key, try to parse (even with None subfields), if not, return CPE field as None
        if data['CPE']:
            # Parse the 'signal' key
            if data['CPE']['signal']:
                for key in data['CPE']['signal'].keys():
                    data['CPE']['signal'][key] = parse_string_to_int(data['CPE']['signal'][key])
        else:
            # For error handing, if the CPE field is not present, return it as None
            data['CPE'] = {key: None for key in CPEStats.__annotations__.keys()}

        # Append the sample to the buffer
        stats.append_stats(data)

    # Show the number of available samples in buffer
    log_message(message=f"Samples available in buffer: {stats.get_samples_available()}", type='DEBUG')

    # Return a confirmation message
    return {"timestamp": get_timestamp(), "message": "Demo stats received"}

# CROWDCELL-RELATED ENDPOINTS ****************************************************

@app.post("/crowdcell/reset_service", tags=["Crowdcell management"])
async def reset_crowdcell():
    '''
    This endpoint sends a http request to the crowdcell to restart service.

    Returns:
    - A dictionary with the response status code {"Response": 200}, if the reset was successful.
    '''

    return await tools.reset_crowdcell(host_address='rest_crowd_host', port='rest_crowd_port', resource='/crowdcell/restartService')

@app.post("/crowdcell/reset_log", tags=["Crowdcell management"])
async def reset_log():
    '''
    This endpoint sends a http request to the crowdcell to reset the log

    Returns:
    - A dictionary with the response status code {"Response": 200}
    '''

    return await tools.reset_crowdcell_log(host_address='rest_crowd_host', port='rest_crowd_port', resource='/amarisoft/enb/log_reset')


@app.get("/crowdcell/get_configuration_file", tags=["Crowdcell management"])
async def get_configuration_file():
    '''
    This endpoint sends a http request to the crowdcell to get the configuration file

    Returns:
    - A dictionary with the response status code {"Response": 200} and the configuration file content
    '''

    return await tools.get_crowdcell_configuration_file(host_address='rest_crowd_host', port='rest_crowd_port', resource='/configuration/all')


@app.get("/crowdcell/get_enb_configuration", tags=["Crowdcell management"])
async def get_enb_configuration():
    '''
    This endpoint sends a http request to the crowdcell to get the eNB configuration

    Returns:
    - A dictionary with the response status code {"Response": 200} and the eNB configuration
    '''

    return await tools.get_crowdcell_enb_configuration(host_address='rest_crowd_host', port='rest_crowd_port', resource='/amarisoft/enb/config_get')

@app.get("/crowdcell/start_stats_monitoring", tags=["Crowdcell monitoring"])
async def start_stats_monitoring():
    '''
    This endpoint sends a http request to the crowdcell to start the stats monitoring

    Returns:
    - A dictionary with the response status code {"Response": 200}
    '''

    return await tools.start_crowd_monitoring(request_type='POST', host_address='rest_crowd_host', port='rest_crowd_port', resource='/monitoring', message='Crowd stats monitoring started')


@app.get("/crowdcell/stop_stats_monitoring", tags=["Crowdcell monitoring"])
async def stop_stats_monitoring():
    '''
    This endpoint sends a http request to the crowdcell to stop the stats monitoring and fetches the stats throughout the monitoring periodç

    Returns:
    - A dictionary with the stats data {"Crowd_stats": List[CrowcellSample]{key:value}}
    '''

    return await tools.stop_crowd_monitoring(request_type='GET', host_address='rest_crowd_host', port='rest_crowd_port', resource='/monitoring', message='Crowd stats monitoring stopped')


@app.get("/crowdcell/start_cpu_monitoring", tags=["Crowdcell monitoring"])
async def start_cpu_monitoring():
    '''
    This endpoint sends a http request to the crowdcell to start the CPU monitoring

    Returns:
    - A dictionary with the response status code {"Response": 200}
    '''

    return await tools.start_crowd_cpu_monitoring(request_type='POST', host_address='rest_crowd_host', port='rest_crowd_port', resource='/resources/monitor/', message='Crowd CPU monitoring started')


@app.get("/crowdcell/stop_cpu_monitoring", tags=["Crowdcell monitoring"])
async def stop_cpu_monitoring():
    '''
    This endpoint sends a http request to the crowdcell to stop the CPU monitoring and fetches the CPU stats throughout the monitoring period

    Returns:
    - A dictionary with the CPU stats data {"CPU_stats": List[ProcessInfo]{key:value}}
    '''

    return await tools.stop_crowd_cpu_monitoring(request_type='GET', host_address='rest_crowd_host', port='rest_crowd_port', resource='/resources/monitor/', message='Crowd CPU monitoring stopped')


@app.get("/crowdcell/initiate_monitoring", tags=["Crowdcell monitoring"])
async def initiate_monitoring(id: Annotated[str, Query()],
                enable_crowd: Annotated[bool, Query()] = True,
                enable_cpe: Annotated[bool, Query()] = True):
    '''
    This endpoint sends a http request to the crowdcell to start the monitoring of CPU and stats

    Returns:
    - A dictionary with a message {"Response": "OK", "Status": "OK"} if the monitoring was successfully started.
    '''
    log_message(message=f"Initiating experiment with ID: {id}", type='DEBUG', bold=True)
    # Set the crowd and cpe invoked flags
    stats.set_crowd_invoked(enable_crowd)
    stats.set_cpe_invoked(enable_cpe)

    # Start the crowd monitoring
    log_message(message=f"Setting crowd flag to {enable_crowd}", type='WARNING')
    if enable_crowd:
        response = await tools.monitor_crowd()
    else:
        response = {"Response": "OK", "Status": True, "Message": "Crowd disabled"}

    
    
    return response


@app.get("/crowdcell/terminate_monitoring", tags=["Crowdcell monitoring"], )
async def terminate_monitoring():
    '''
    This endpoint sends a http request to the crowdcell to stop the monitoring and fetches the stats throughout the monitoring period

    Returns:
    - A dictionary with the response status code {"Response": 200} and stats
    '''

    return await tools.terminate_monitoring_crowd()


@app.post("/crowdcell/configure_gain", tags=["Crowdcell configuration"])
async def configure_gain(gain: Annotated[int, Query(le=0, ge=-100)]):
    '''
    This endpoint sends a http request to the crowdcell to configure the gain

    Parameters:
    - gain: int. The gain value to be set

    Returns:
    - A dictionary with the response status code {"Response": 200}
    '''

    return await tools.set_gain(gain=gain, host_address='rest_crowd_host', port='rest_crowd_port', resource='/amarisoft/enb/cell_gain')


@app.post("/crowdcell/configure_noise_level", tags=["Crowdcell configuration"])
async def configure_noise_level(noise_level: Annotated[int, Query(le=0, ge=-30)]):
    '''
    This endpoint sends a http request to the crowdcell to configure the noise level

    Parameters:
    - noise_level: int. The noise level value to be set

    Returns:
    - A dictionary with the response status code {"Response": 200}
    '''

    return await tools.set_noise_level(noise_level=noise_level, host_address='rest_crowd_host', port='rest_crowd_port', resource='/amarisoft/enb/noise_level')


@app.post("/crowdcell/configure_resources", tags=["Crowdcell configuration"])
async def configure_resources(prbs: Annotated[int, Query(le=106, ge=0)],
                              rb_start: Annotated[int, Query(le=106, ge=0)],
                              cell_id: Annotated[int, Query(le=20, ge=0)] = 1):
    '''
    This endpoint sends a http request to the crowdcell to configure the resources

    Parameters:
    - prbs: int. The PRBS value to be set
    - rb_start: int. The RB start value to be set
    - cell_id: int, default=1. The cell ID value to be set

    Returns:
    - A dictionary with the response status code {"Response": 200}
    '''

    return await tools.set_prbs(prbs=prbs, rb_start=rb_start, cell_id=cell_id, host_address='rest_crowd_host', port='rest_crowd_port', resource='/amarisoft/enb/config_set')


@app.post("/crowdcell/configure_mcs", tags=["Crowdcell configuration"])
async def configure_mcs(mcs: Annotated[int, Query(le=28, ge=0)],
                        cell_id: Annotated[int, Query(le=20, ge=0)] = 1):
    '''
    This endpoint sends a http request to the crowdcell to configure the MCS

    Parameters:
    - mcs: int. The MCS value to be set

    Returns:
    - A dictionary with the response status code {"Response": 200}
    '''

    return await tools.set_mcs(mcs=mcs, cell_id=cell_id, host_address='rest_crowd_host', port='rest_crowd_port', resource='/amarisoft/enb/config_set')