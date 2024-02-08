from fastapi import FastAPI, Query, Path, Body
from typing import Annotated
from .models import SessionStats, example_POST_testbed, SampleStats, CPEStats, example_POST_demo
from .Stats import Stats
from .utils import *
from .sample_generator import SyntheticSample as Synthetic
from config_params import ConfigManager

stats = Stats(n_samples=ConfigManager.get_parameters('rest_n_samples'))
app = FastAPI()


@app.get("/awake")
async def awake():
    return {"message": "The server is awake"}


@app.get("/video360/demo")
async def get_samples(n_items: Annotated[int, Query(le=ConfigManager.get_parameters('rest_n_samples'))] = 1,
                      cpe: Annotated[bool, Query()] = False):
    # If the number of items is equal or less than n_samples, get n_samples from stats buffer
    data = stats.get_items(end=n_items, cpe=cpe)
    return data


@app.get("/video360/generate_sample")
async def get_synthetic_sample(cpe: Annotated[bool, Query()] = False):
    # Create a fake sample using KQI model format
    data = Synthetic.generate_sample(cpe=cpe)
    return data


@app.post("/video360/testbed/{timestamp}")
async def save_session(timestamp: Annotated[int, Path(ge=0)],
                       data: Annotated[SessionStats | None, Body(examples=[example_POST_testbed])]):
    # Parse body data as dict-base json
    data_json = data.model_dump()
    print(f"{get_time()} REST SERVER --> (Received: \n {data_json}")
    # Write and save as a JSON file in the data folder
    path_file = generate_file_path(str(timestamp), get_local_data_path())
    write_file(path_file, content=data_json, mode='w')
    # Return a confirmation message
    return {"timestamp": timestamp, "message": "Session stats received"}


@app.post("/video360/demo/")
async def append_sample(data: Annotated[SampleStats | None, Body(examples=[example_POST_demo])] = None):
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
    print(f"{get_time()} REST SERVER --> Samples available in buffer: {stats.get_samples_available()}")
    # Return a confirmation message
    return {"timestamp": get_timestamp(), "message": "Demo stats received"}
