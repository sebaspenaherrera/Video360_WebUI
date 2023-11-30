from components.elements.charts.chart import *
from config_params import ConfigManager


def get_data(n_samp: int = 1, cpe: bool = False):
    base = "http://" + ConfigManager.get_parameters('rest_host') + ":" + str(ConfigManager.get_parameters('rest_port'))
    header = {'content-type': 'application/json'}
    query = {}
    # For normal DEMO mode, use the /demo path
    if not ConfigManager.get_parameters('web_test'):
        url = "/video360/demo"
    else:
        # For UI testing purposes, it is possible to get fake samples from the REST using the /generate_sample path
        url = "/video360/generate_sample"

    # If query params are required, add query params in the url
    if n_samp > 1:
        query.update({'n_items': n_samp})
    if cpe:
        query.update({'cpe': cpe})

    # Try to send a GET request to the rest server and fetch a sample stats
    try:
        r = requests.get(base + url, timeout=5, headers=header, params=query)
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
    return generate_fig_live(ConfigManager.get_parameters('datVR'), value)


def update_data(n):
    # Read current state of the CPE flag
    cpe = ConfigManager.get_parameters('web_cpe')
    n_samp = int(ConfigManager.get_parameters('t_interval') / 1000)
    # Get Data from the REST
    data = get_data(n_samp=n_samp, cpe=cpe)

    if data:
        print(data)
        # Check if the received dict-json data is a list or a dict
        if isinstance(data, list):
            data = data[-1]
            d = data['Service']
        else:

            d = data['Service']

        # If cpe flag is active, parse the CPE stats
        if cpe:
            # Append the CPE stats to the dict
            d.update(parse_cpe_stats(data))

    # Check if the received dict-json data is not empty
    if d:
        ConfigManager.update_parameters('n_IVR', n)
        now = datetime.now().strftime("%H:%M:%S")
        d.update({'datetime': now})
        print(f"(Web UI) --> {now} Updating...")
        # Update the global variable with the new sample
        print(d)
        x = pd.concat([ConfigManager.get_parameters('datVR'),
                       pd.DataFrame.from_dict(d, orient='index').T], ignore_index=True)
        # Update the global variable with the new sample

        ConfigManager.update_parameters('datVR', x)

        # If the number of samples is greater than the maximum number of samples, remove the first sample
        if len(ConfigManager.get_parameters('datVR')) == ConfigManager.get_parameters('max_samples'):
            ConfigManager.update_parameters('datVR', ConfigManager.get_parameters('datVR')[1:])

        # Update the global variable with the new sample
        return ConfigManager.get_parameters('n_IVR')


# Update timer interval
def update_interval(value):
    # Update the global variable with the new interval in milliseconds
    ConfigManager.update_parameters('t_interval', 1000 * value)
    print('EVENT: ------- Interval set to: {} ms --------'.format(ConfigManager.get_parameters('t_interval')))
    return ConfigManager.get_parameters('t_interval')
    # return params.t_interval


# Extract CPE stats from REST
def parse_cpe_stats(value):
    # If CPE stats exist, get all the numeric values
    cpe_stats = {}

    if value['CPE']:
        # Iterate over the CPE stats and get the numeric values
        for parameter in value['CPE'].keys():
            for metric in value['CPE'][parameter].keys():
                if isinstance(value['CPE'][parameter][metric], (int, float)):
                    cpe_stats.update({metric: value['CPE'][parameter][metric]})
    # Return the CPE stats
    return cpe_stats

