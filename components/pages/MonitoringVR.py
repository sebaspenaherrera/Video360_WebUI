from components.elements.charts.chart import *

# CSS

contentStyle = {"display": "inline-block", "padding": "0px 0px 0px 0px", "padding-top": "10px", "width": "100%"}

########################################
#           Component's content
########################################


dropMenuCharts = list(VR_QOE.keys())

content = html.Div(id="measuresContent", children=[
    dbc.Row(
        [
            get_chart(id="vr_f1", menu=dropMenuCharts, initial_value="height"),
            get_chart(id="vr_f2", menu=dropMenuCharts, initial_value="displayed_frameRate"),
            get_chart(id="vr_f3", menu=dropMenuCharts, initial_value="screen_frameRate"),
            get_chart(id="vr_f4", menu=dropMenuCharts, initial_value="res_switches")
        ]
    ),

    dbc.Row(
        [
            get_chart(id="vr_f5", menu=dropMenuCharts, initial_value="initTime"),
            get_chart(id="vr_f6", menu=dropMenuCharts, initial_value="rx_rate"),
            get_chart(id="vr_f7", menu=dropMenuCharts, initial_value="bufferTime"),
            get_chart(id="vr_f8", menu=dropMenuCharts, initial_value="rtt")
        ]
    ),

    ],
    style=contentStyle
)


def get_monitoring_component():
    component = html.Div(id="measuresComponentVR", children=[content], style={'width': "auto"})
    return component
