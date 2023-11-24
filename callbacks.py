import config_params
from components.elements.charts.chart import *
from config_params import *


def get_data(n_samp: int = 1, cpe: bool = False):
    base = "http://" + rest_host + ":" + str(rest_port)
    header = {'content-type': 'application/json'}
    query = {}
    # url = "/video360/demo"
    url = "/video360/generate_sample"

    # If query parameters are required, add query parameters in the url
    if n_samp > 1:
        query.update({'n_items': n_samp})
    if cpe:
        query.update({'cpe': cpe})

    # Try to send a GET request to the rest server and fetch a sample stats
    try:
        r = requests.get(base + url, timeout=10, headers=header, params=query)
        return r.json()
    except ConnectionError or TimeoutError:
        traceback.print_exc()
        print(f"(Web UI) --> REST unavailable at {base + url}")
        try:
            print(f"(Web UI) --> Trying to request again to REST at {base + url}")
            r = requests.get(base + url, timeout=10, headers=header)
            return r.json()
        except ConnectionError or TimeoutError:
            print("(Web UI) --> Something wrong")
            return {}


def update_live_graph(d, value):
    return generate_fig_live(config_params.datVR, value)


def update_data(n):
    # Get Data from the REST
    d = get_data()['Service']
    print(f"DATA OBTAINED FROM REST = \n {d}")
    # Check if the received dict-json data is not empty
    if d:
        config_params.n_IVR = n
        now = datetime.now().strftime("%H:%M:%S")
        d.update({'datetime': now})
        print(f"(Web UI) --> {now} Updating...")
        print(pd.DataFrame.from_dict(d, orient='index'))
        config_params.datVR = pd.concat([config_params.datVR, pd.DataFrame.from_dict(d, orient='index').T],
                                        ignore_index=True)
        print(f"(Web UI) --> Data: {config_params.datVR}")
        if len(config_params.datVR) == config_params.max_samples:
            config_params.datVR = config_params.datVR[1:]

    return config_params.n_IVR


# Update timer interval
def update_interval(value):
    # Global variable for timerInterval
    config_params.t_interval = 1000 * value
    print('EVENT: ------- Interval set to: {} --------'.format(config_params.t_interval))
    return config_params.t_interval
