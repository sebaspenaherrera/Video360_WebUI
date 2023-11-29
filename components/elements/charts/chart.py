from dependencies import *
from data.VR_metadata import *

parameters = dict()
units = dict()

# VR
parameters.update(VR_QOE)
units.update(VR_UNITS)

# CSS
CHART_STYLE = {
    'display': 'auto',
    'text-align': 'center',
    'width': '100%',
    'padding': '0px 0px 0px 0px',
    'margin': '0px 0px 0px 0px'
}


def generate_fig(value):
    # Try to create a Figure object from Plotly express
    try:
        fig = go.Figure()
    # If "go" object returns an exception, try to draw again with a default value
    except:
        fig = go.Figure()
        fig.update_layout(
            margin=dict(l=5, r=5, t=5, b=5),
            plot_bgcolor="#FEF9E7",
            yaxis_title=units[value],
            height=200
        )
    return fig


def get_chart(id, menu, initial_value):
    # Plotly Express
    # Metrics is a list with the metrics to show in the dropdown menu
    drop_menu = []
    for x in menu:
        # dropMenu.append({'label': x, 'value': x})
        drop_menu.append({'label': VR_TAGS[x], 'value': x})

    fig = generate_fig(initial_value)

    return dbc.Col(html.Div(id=id, children=[
        dcc.Dropdown(id="dropdown_" + id,
                     options=drop_menu,
                     multi=False,
                     value=initial_value,
                     style={'display': 'relative', 'width': "100%", 'text-align': 'center', 'margin-bottom': '0px',
                            "border-color": "#FDEBD0"}
                     ),
        dcc.Graph(id='chart_' + id, figure=fig, config={
            'displayModeBar': False, 'autosizable': True
        }, style={'padding': '0px', 'height': '100%', 'width': "100%", 'text-align': 'center'})
    ], style=CHART_STYLE))


def generate_fig_live(d, value):
    if len(d) > 10:
        d = d[-10:]
    try:
        data = d[parameters[value]]
    except:
        data = []

    try:
        fig = go.Figure(data=go.Scatter(x=d['datetime'], y=data, mode="lines+markers",
                                        line_shape='linear', name="Measured",
                                        )
                        )
    except:

        fig = go.Figure(data=go.Scatter(x=np.arange(len(data)), y=data, mode="lines+markers",
                                        line_shape='linear'))
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor="#FEF9E7",
        yaxis_title=units[value],
        height=200
    )

    fig = chart_axis(fig, value)
    return fig


def chart_axis(fig, value):
    if value == "resolution":
        fig.update_yaxes(categoryarray=['360p', '540p', '720p', '1080p', '1440p', '4K'],
                         categoryorder="array", range=[-0.5, 6.5])

    '''elif value == 'screen_frameRate':
        fig.update_yaxes(range=[69, 76], dtick=2)'''

    '''elif value == 'initTime' or value == 'stallTime' or value == 'overallStallTime':
        fig.update_yaxes(rangemode="nonnegative", range=[-0.5, 5])'''

    return fig
