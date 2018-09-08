from dash_core_components import Slider
from dash_html_components import Div, H3
from dash.dependencies import Input, Output

from brewlog import dash_app


dash_app.layout = (
        Div(className='panel panel-default', children=[

            # placeholder for figure
            Div(id='target', className='panel-body step-panel'),

            # slider for the grind size
            Div(className='panel-body step-panel', children=[
                H3('Grind size'),
                Slider(id='grind-slider', min=1, max=10, step=1, value=3,
                       marks={str(i): str(i) for i in range(1, 11)})]),

            # slider for the water cool time
            Div(className='panel-body step-panel', children=[
                H3('Water cool time '),
                Slider(id='water-slider', min=0, max=60, step=10, value=20,
                       marks={str(i): str(i) for i in range(0, 70, 10)})]),
        ])
)


@dash_app.callback(Output('target', 'children'),
                   [Input('grind-slider', 'value'),
                    Input('water-slider', 'value')])
def callback(value1, value2):
    return "callback received value: {}".format(value1)
