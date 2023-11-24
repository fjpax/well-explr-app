import dash
from dash import Input, Output, State, html, Dash, callback, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import os
# Import necessary libraries 
from utils.viz_wellpath import viz_wellpath_plot
###########
import dash_daq as daq
import plotly.graph_objects as go

dash.register_page(__name__)


###########
xx = os.listdir('all_survey_csv')
xx = os.listdir('all_suervey_withoutaker')

try:
    xx.remove('.DS_Store')
except:
    pass
x=list(map(lambda cur: cur[:-4],xx))
well_survey_ops = []
for op in set(x):
   well_survey_ops.append({'label':str(op),'value':op})
well_survey_ops

########




dropdowns = html.Div(
    [   dbc.Row([html.H3('Well Names', style={'margin-left': '10px'})]),
        dbc.Row([dcc.Dropdown(id='Well_option',
                    options=well_survey_ops
                    ,placeholder='Well_options'
                    ,value = ['15_9-F-15', '15_9-F-11 A']
                    ,multi=True, style={'width': '500px','margin-left': '10px'})]),
                
           dbc.Row([daq.BooleanSwitch(
                                id ='show_dls_switch',
                                on=False,
                                label='Dogleg Severity',
                                labelPosition="top",
                                style={'margin-left': '10px'}
                                )]),
             
              dbc.Row([daq.BooleanSwitch(
                                id ='show_incidents_switch',
                                on=True,
                                label='Reports',
                                labelPosition="top",
                                style={'margin-left': '10px'}
                                ),
                
                                            
                # html.Div(html.Button(id='My_button', 
                #         n_clicks=0, 
                #         children='Display', 
                #         style={'fontSize':20,'display':'inline-block'})
                #     )
        ])

       
    ],
    
)




layout = dbc.Container ([html.Div([
            dbc.Row([
                dbc.Button(
                    "Show Filter",
                    id="collapse_button_drilling",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                   
                    dropdowns,
                    
                    id="collapse_drilling",
                    is_open=False,
                  
                    style= {"background-color": "LightGrey",'height': '100vh', 'width': '100vh'}
                )]),
            dbc.Row([
                    dbc.Col([
                            dcc.Graph(id='survey_plot',style={ 'marginBottom': 200, 'height': '100vh', 'width': '100vh'})
                            ] ),#,width = 9
                    
                    # dbc.Col([
                    #         dcc.Graph(style={ 'height': '100%'})
                    #         ] ,width = 3)
                    
                    
                    ])            
            

                ],style = {'width': '100vh', 'height': '100vh'}) ],
   fluid=True,style={'marginBottom': 200, 'width': '100vh', 'height': '100vh'})

@callback(
    Output("collapse_drilling", "is_open"),
    [Input("collapse_button_drilling", "n_clicks")],
    [State("collapse_drilling", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



# @callback(
#     [Output("survey_plot", "figure")],
#     #[Input('My_button','n_clicks'),

#     [Input("show_dls_switch",'on' ),
#      Input("show_incidents_switch",'on' )],
#     [State('Well_option', "value")],
# )

@callback(
    [Output("survey_plot", "figure")],
    #[Input('My_button','n_clicks'),

    [Input("show_dls_switch",'on' ),
     Input("show_incidents_switch",'on' ),
     Input('Well_option', "value")],
    
)
#def plot_data(n_clicks, show_dls, show_incidents, well_name_chosen):
def plot_data(show_dls, show_incidents, well_name_chosen):    

    return [viz_wellpath_plot(well_name_chosen, show_dogleg=show_dls, show_incidents=show_incidents)]






