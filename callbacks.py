from components.elements.charts.chart import *
from config_params import ConfigManager


def get_data(n_samp: int = 1, cpe: bool = False):
    base = "http://" + ConfigManager.get_parameters('rest_host') + ":" + str(ConfigManager.get_parameters('rest_port'))
    header = {'content-type': 'application/json'}
    query = {}
    # For normal DEMO mode, use the /demo path
    print(ConfigManager.get_parameters('web_test'))
    if not ConfigManager.get_parameters('web_test'):
        url = "/video360/demo"
    else:
        # For UI testing purposes, it is possible to get fake samples from the REST using the /generate_sample path
        url = "/video360/generate_sample"
    print("CPE ACTIVO!!!" + str(cpe))
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
    # return generate_fig_live(params.datVR, value)


def update_data(n):
    # Get Data from the REST
    print("Que pasa: " + str(ConfigManager.get_parameters('web_cpe')))
    d = get_data(cpe=ConfigManager.get_parameters('web_cpe'))

    if d:
        if isinstance(d, list):
            d = d[0]
        else:
            d = d['Service']

    # Check if the received dict-json data is not empty
    if d:
        ConfigManager.update_parameters('n_IVR', n)
        now = datetime.now().strftime("%H:%M:%S")
        d.update({'datetime': now})
        print(f"(Web UI) --> {now} Updating...")
        # Update the global variable with the new sample
        x = pd.concat([ConfigManager.get_parameters('datVR'),
                       pd.DataFrame.from_dict(d, orient='index').T], ignore_index=True)
        print(x)
        ConfigManager.update_parameters('datVR', x)
        '''params.datVR = pd.concat([params.datVR, pd.DataFrame.from_dict(d, orient='index').T],
                                 ignore_index=True)'''
        # If the number of samples is greater than the maximum number of samples, remove the first sample
        if len(ConfigManager.get_parameters('datVR')) == ConfigManager.get_parameters('max_samples'):
            ConfigManager.update_parameters('datVR', ConfigManager.get_parameters('datVR')[1:])
        '''if len(params.datVR) == params.max_samples:
            params.datVR = params.datVR[1:]'''

        # Update the global variable with the new sample
        return ConfigManager.get_parameters('n_IVR')
    # return params.n_IVR


# Update timer interval
def update_interval(value):
    ConfigManager.update_parameters('t_interval', 1000 * value)
    # params.t_interval = 1000 * value
    print('EVENT: ------- Interval set to: {} ms --------'.format(ConfigManager.get_parameters('t_interval')))
    # print('EVENT: ------- Interval set to: {} ms --------'.format(params.t_interval))
    return ConfigManager.get_parameters('t_interval')
    # return params.t_interval
