'''
Skeleton for the monitoring app

The monitoring app is a web-based application that displays the VR data in real-time. The app is built using Dash, and it is responsible for displaying the VR data in a user-friendly way. 
The app consists of several components, such as dropdowns, sliders, and graphs, that allow the user to interact with the data and customize the display.

Version: 1.0. Original skeleton version of Carlos Baena. Updated to ASGI by Sebastian Peñaherrera
'''

from callbacks import *
from components.elements.menus.menu_nav import *
from pagesManagement import *
import dash_daq as daq
import dash_bootstrap_components as dbc
from config_params import ConfigManager

# APP INITIALIZATION
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], suppress_callback_exceptions=True,
                requests_pathname_prefix='/monitoring/')

# PAGE CONTENT STYLE (CSS)
PAGE_CONTENT = {
    "padding": "0px",
    "background-color": "#FDFEFE"
}

# APP LAYOUT
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),

    # Timers
    dcc.Interval(
        id='timerVR',
        interval=ConfigManager.get_parameters('t_interval'),  # in milliseconds, by default
        n_intervals=0
    ),

    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(nav()),
                    dbc.Col(),
                    dbc.Col("Interval: ", align="end", width="auto"),
                    dbc.Col(
                        daq.Slider(
                            id='refreshTime',
                            min=1,
                            max=10,
                            step=1,
                            value=2,
                            marks={
                                2: '2',
                                4: '4',
                                6: '6',
                                8: '8',
                                10: '10'
                            },
                            size=300
                        ),
                        align="center"
                    ),
                ],
                justify="end"
            )
        ]
    ),

    html.Hr(),
    html.Div(id="page-content", style=PAGE_CONTENT),
    html.Hr(),

    html.Img(src="./assets/MobilenetLogo.png", width="150px", style={"margin-left": "0px"}),
    html.Img(src="./assets/TelmaLogo.png", width="150px", style={"margin-left": "30px"}),
    html.Img(src="./assets/uma.png", width="100px", style={"margin-left": "30px"}),
    html.Img(src="./assets/juntaAndalucia.svg", width="120px", style={"margin-left": "30px"}),
    html.Img(src="./assets/PlanRecuperacionLogo.png", width="150px", style={"margin-left": "30px"}),
    html.Img(src="./assets/UnicoLogo.png", width="130px", style={"margin-left": "30px"}),
    html.Img(src="./assets/FundedbyEULogo.png", width="150px", style={"margin-left": "30px"}),
    html.Img(src="assets/Mobilenet_QR_text.png", width="150px", style={"margin-left": "10px"}),

    # Hidden variables
    html.Div(id="var_data", style={'display': 'none'}),

])

###################################################################################################
#                                       CALLBACKS Definitions
###################################################################################################

# Page management
app.callback(Output('page-content', 'children'),
             Input('url', 'pathname'))(display_monitoring_page)

# VR chart update
for graph in range(1, 9):
    app.callback(Output(component_id='chart_vr_f' + str(graph), component_property='figure'),
                 Input(component_id="var_data", component_property='children'),
                 Input(component_id='dropdown_vr_f' + str(graph), component_property='value')
                 )(update_live_graph)

# Update vr data
app.callback(Output(component_id="var_data", component_property='children'),
             Input(component_id='timerVR', component_property='n_intervals')
             )(update_data)

# Callback for slider value-changing
app.callback(Output(component_id='timerVR', component_property='interval'),
             Input(component_id='refreshTime', component_property='value')
             )(update_interval)

if __name__ == "__main__":
    app.run_server(debug=True)

