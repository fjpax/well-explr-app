import dash
from dash import html, dcc
from dash import Input, Output, State, html, Dash, callback

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash
from dash_bootstrap_components._components.Container import Container





dash.register_page(__name__)
# Import necessary libraries 
from dash import html
import dash_bootstrap_components as dbc

###########
from utils.ave_ROP_Depth import viz_averop_formation

import os
#xx = os.listdir('/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_with_fm_csv')
xx = os.listdir('/Users/2924441/Desktop/phd part 2/add_fm_data/all_fm')
try:
    xx.remove('.DS_Store')
except:
    pass
x=list(map(lambda cur: cur[:-4],xx))
well_formation_ops = []
for op in set(x):
   well_formation_ops.append({'label':str(op),'value':op})
well_formation_ops


########



dropdowns = html.Div(
    [
        dbc.Row([dcc.Dropdown(id='Well_option_strat',
                    options=well_formation_ops
                    ,placeholder='Well_options'
                    ,multi=True, style={'width': '370px'}),
                
                html.Div(html.Button(id='my_button_strat', 
                        n_clicks=0, 
                        children='Display', 
                        style={'fontSize':20,'display':'inline-block'})
                    )
        ])

       
    ],
    
)


layout = html.Div([
            dbc.Row([
                dbc.Button(
                    "Show Filter",
                    id="collapse_button_strat",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                   
                    dropdowns,
                    
                    id="collapse_strat",
                    is_open=False,
                )]),
            dbc.Row([dcc.Graph(id="survey_plot_strat")])            


                ])

@callback(
    Output("collapse_strat", "is_open"),
    [Input("collapse_button_strat", "n_clicks")],
    [State("collapse_strat", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



@callback(
    [Output("survey_plot_strat", "figure")],
    [Input('my_button_strat','n_clicks')],
    [State('Well_option_strat', "value")],
)
def plot_data(n_clicks, well_name_chosen):
    
    return [viz_averop_formation(well_name_chosen)]






