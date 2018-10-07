import json

import pandas as pd

from dash_core_components import Slider
from dash_html_components import Div, H3, Button, Img
from dash.dependencies import Input, Output

from brewlog import app, dash_app
from brewlog.db_io import load_wide_table, calculate_features
from brewlog.optimize import (make_gp_model, make_prediction_grid,
                              make_predictions)
from brewlog.plots import plot_predictions


dash_app.layout = (
        Div(className='panel panel-default', children=[

            # placeholder for figure
            Div(id='target', className='panel-body step-panel', children=[
                Img(id='fig-img', className="img-responsive center-block")]),

            # button to load data
            # need to do this so that current_user is populated before we query
            Div(className='panel-body step-panel', children=[
                Button('Load data', id='load-data-button')]),

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

            # hidden div to hold json-ified wide table data
            # see https://dash.plot.ly/sharing-data-between-callbacks
            Div(id='data-container-wide-table', style={'display': 'none'}),
        ])
)


@dash_app.callback(Output('data-container-wide-table', 'children'),
                   [Input('load-data-button', 'n_clicks')])
def load_data_callback(n_clicks):

    app.logger.info('load_data_callback fired')

    # this gets triggered on page load, but n_clicks will be None 
    if n_clicks:
        return load_wide_table().to_json(orient='split', date_format='iso')


# @dash_app.callback(Output(component_id='fig-img', component_property='src'),
#                    [Input('data-container-wide-table', 'children')])
# def show_plot_callback(jsonified_df):
# 
#     app.logger.info('show_plot_callback fired')
# 
#     # the load_data callback gets triggered on page load for some reason
#     # which triggers this, so we have to short circuit until we get data
#     if not jsonified_df:
#         return None
# 
#     wide = pd.read_json(jsonified_df, orient='split')
# 
#     print(wide.columns)
#     print(wide.dtypes)
# 
#     features = calculate_features(wide)
# 
#     return plot_time_vs_ratio(features)


@dash_app.callback(Output(component_id='fig-img', component_property='src'),
                   [Input('data-container-wide-table', 'children'),
                    Input('grind-slider', 'value'),
                    Input('water-slider', 'value')])
def show_heatmap_callback(jsonified_df, grind_slice, water_slice):

    app.logger.info('show_heatmap_callback fired')

    # the load_data callback gets triggered on page load for some reason
    # which triggers this, so we have to short circuit until we get data
    if not jsonified_df:
        return None

    # read the loaded data and calculate some derived features
    wide = pd.read_json(jsonified_df, orient='split')
    features = calculate_features(wide)

    # fit a model to the data, discretize the parameter space, then
    # score the model on each point in the discretized parameter space
    model = make_gp_model(features)
    coords = make_prediction_grid()
    preds = make_predictions(model, coords)

    return plot_predictions(preds, grind_slice, cool_slice)
