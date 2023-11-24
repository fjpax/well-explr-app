import dash
from dash import Input, Output, State, html, Dash, callback, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import os
# Import necessary libraries 
from utils.viz_wellpath import viz_wellpath_plot
###########
import dash_daq as daq
from utils.daily_operation_report import daily_report_sun

dash.register_page(__name__)

import pickle

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




# dropdowns = html.Div(
#     [
#         dbc.Row([dcc.Dropdown(id='well_comparer1',
#                     options=well_survey_ops
#                     ,placeholder='Well_options'
#                     ,value = '15_9-F-15'
#                     ,multi=False, style={'width': '370px'}),
                
#                 dcc.Dropdown(id='well_comparer2',
#                     options=well_survey_ops
#                     ,placeholder='Well_options'
#                     ,value = '15_9-F-11 A'
#                     ,multi=False, style={'width': '370px'}),
                
                                            
#                 html.Div(html.Button(id='well_comparer_My_button', 
#                         n_clicks=0, 
#                         children='Display', 
#                         style={'fontSize':20,'display':'inline-block'})
#                     )
#         ])

       
#     ],
    
# )





layout = dbc.Container([html.Div([
               # html.Div([dropdowns]), 
                html.Br(),
                dbc.Row([
                        dbc.Col([
                                
                                ], md=1 ),
                        dbc.Col([
                              dcc.Dropdown(id='well_comparer1',
                                                options=well_survey_ops
                                                ,placeholder='Well_options'
                                                ,value = '15_9-F-15'
                                                ,multi=False, 
                                                 style={'width':'100%', 'display':'inline-block'}),
                                                ],md=5),


                        dbc.Col([
                               dcc.Dropdown(id='well_comparer2',
                                                options=well_survey_ops
                                                ,placeholder='Well_options'
                                                ,value = '15_9-F-11 A'
                                                ,multi=False, 
                                                style={'width':'100%', 'display':'inline-block'})
                                                                ],md=5),]),
              
                dbc.Row([
                        dbc.Col([
                                html.H4('Survey', style={'textAlign':"left"})
                                ], md=1 ),
                        dbc.Col([
                                dcc.Graph(id='well_comparer_survey_plot1')
                                ],md=5 ),#,width = 9
                                
                        dbc.Col([
                                dcc.Graph(id='well_comparer_survey_plot2')
                                ] ,md=5),]),



              
                html.Hr(style={"align": "center","width":"100%"}),
                dbc.Row([
                        dbc.Col([
                                html.H4('Daily Report', style={'textAlign':"left"})
                                ], md=1 ),
                        dbc.Col([
                                dcc.Graph(id='well_comparer_dr_plot1')
                                ],md=5 ),#,width = 9
                                
                        dbc.Col([
                                dcc.Graph(id='well_comparer_dr_plot2')
                                ] ,md=5),]),



                html.Hr(style={"width":"100%","text-align": "right"}),
                dbc.Row([
                        dbc.Col([
                                html.H4('Well Type', style={'textAlign':"left"})
                                ], md=1 ),
                        dbc.Col([
                                html.P(id= 'Well_type_text1', style={"color": "gray",'textAlign':"center"})
                                ],md=5 ),
                                
                        dbc.Col([
                                html.P(id= 'Well_type_text2', style={"color": "gray",'textAlign':"center"})
                                ] ,md=5),]),





                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Purpose', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Purpose_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Purpose_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),



                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Status', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Status_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Status_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),
                

                #multilateral
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Multilateral', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Multilateral_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Multilateral_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),

                
                #'Production licence'
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Production licence', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Production licence_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Production licence_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),
                
                #'Drilling operator',
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Drilling operator', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Drilling operator_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Drilling operator_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),
                


                #'Drilling facility',  '', 'Entered date', 'Completed date'
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Drilling facility', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Drilling facility_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Drilling facility_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),

                #'Production facility'
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Production facility', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Production facility_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Production facility_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),

                
                #'Drilling days'
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Drilling days', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Drilling days_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Drilling days_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),


                #'Entered date'
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Entered date', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Entered date_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Entered date_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),
                

                #'Entered date'
                html.Hr(style={"width":"100%","align": "right"}),
                dbc.Row([
                    dbc.Col([
                           html.H4('Completed date', style={'textAlign':"left"})
                            ], md=1 ),
                    dbc.Col([
                             html.P(id= 'Completed date_text1', style={"color": "gray",'textAlign':"center"})
                            ],md=5 ),
                        
                    dbc.Col([
                            html.P(id= 'Completed date_text2', style={"color": "gray",'textAlign':"center"})
                            ] ,md=5),]),


                
                    
                    




                      
            

                         ],style = {'display': 'inline-block', 'width': '100%', 'height': '100%'}) ],
                    fluid=False,style={"height": "100vh"})#style={'marginBottom': 100, 'width': '100%', 'height': '100%'})




@callback(
    [Output('well_comparer_survey_plot1', "figure"), Output( 'well_comparer_survey_plot2', "figure"),
    Output('well_comparer_dr_plot1', "figure"),Output( 'well_comparer_dr_plot2', "figure"),
    Output('Well_type_text1', "children"),Output( 'Well_type_text2', "children"),
    Output('Purpose_text1', "children"),Output( 'Purpose_text2', "children"),
    Output('Status_text1', "children"),Output( 'Status_text2',"children"),
    Output('Multilateral_text1', "children"),Output( 'Multilateral_text2', "children"),
    Output('Production licence_text1', "children"),Output( 'Production licence_text2', "children"),
    Output('Drilling operator_text1', "children"),Output( 'Drilling operator_text2', "children"),
    Output('Drilling facility_text1', "children"),Output( 'Drilling facility_text2', "children"),
    Output('Production facility_text1', "children"),Output( 'Production facility_text2', "children"),
    Output('Drilling days_text1', "children"),Output( 'Drilling days_text2', "children"),
    Output('Entered date_text1', "children"),Output( 'Entered date_text2', "children"),
    Output('Completed date_text1', "children"),Output( 'Completed date_text2', "children"),
    
    
    
    
    ],



   # [Input('well_comparer_My_button','n_clicks')],


    [Input('well_comparer1', "value")],
    [Input('well_comparer2', "value")]
    )
#def well_comparer_plot_data(n_clicks, well_comparer1, well_comparer2):
def well_comparer_plot_data( well_comparer1, well_comparer2):
        print(well_comparer1, well_comparer2)


        all_info_dict= pickle.load(open("npd_overall/dev_wells_info.pkl", "rb"))
        print(all_info_dict[well_comparer1]['Type'])
        print(all_info_dict[well_comparer1]['Purpose'])
     
        return [viz_wellpath_plot([well_comparer1], show_dogleg=False, show_incidents=True),viz_wellpath_plot([well_comparer2], show_dogleg=False, show_incidents=True),
            daily_report_sun(well_comparer1),daily_report_sun(well_comparer2),
                all_info_dict[well_comparer1]['Type'],all_info_dict[well_comparer2]['Type'],
                all_info_dict[well_comparer1]['Purpose'],all_info_dict[well_comparer2]['Purpose'],
                all_info_dict[well_comparer1]['Status'],all_info_dict[well_comparer2]['Status'],
            all_info_dict[well_comparer1]['Multilateral'],all_info_dict[well_comparer2]['Multilateral'],
        all_info_dict[well_comparer1]['Production licence'],all_info_dict[well_comparer2]['Production licence'],
        all_info_dict[well_comparer1]['Drilling operator'],all_info_dict[well_comparer2]['Drilling operator'],
        all_info_dict[well_comparer1]['Drilling facility'],all_info_dict[well_comparer2]['Drilling facility'],
        all_info_dict[well_comparer1]['Production facility'],all_info_dict[well_comparer2]['Production facility'],
        all_info_dict[well_comparer1]['Drilling days'],all_info_dict[well_comparer2]['Drilling days'],
        all_info_dict[well_comparer1]['Entered date'],all_info_dict[well_comparer2]['Entered date'],
        all_info_dict[well_comparer1]['Completed date'],all_info_dict[well_comparer2]['Completed date'],
            ]



