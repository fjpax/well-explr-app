import dash
from dash import Input, Output, State, html, Dash, callback, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import os
import pandas as pd
# Import necessary libraries 
import pickle
###########

#   
#casing design dict
well_casing_design_all_dict= pickle.load(open("npd_overall/casingData3.pkl", "rb"))

#strat_dict
stratigraphy_all_dict = pickle.load(open("npd_overall/wellStratigraphy.pkl", "rb"))




well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')
well_data = well_data_orig.copy() 
well_data['wlbContent'] = well_data['wlbContent'].fillna('NO DATA')
explo_df = well_data



field_options= []
for op in pickle.load(open("npd_overall/field_names_list.pkl", "rb")):
    field_options.append({'label':str(op),'value':op})

well_type_options= []
for op in ['EXPLORATION','DEVELOPMENT']:
    well_type_options.append({'label':str(op),'value':op})

well_operator_options_ex= []
for op in explo_df['wlbDrillingOperator'].unique():
    well_operator_options_ex.append({'label':str(op),'value':op})
    

well_wlbPurpose = []
for op in explo_df['wlbPurpose'].unique():
    well_wlbPurpose.append({'label':str(op),'value':op})


well_wlbStatus = []
for op in explo_df['wlbStatus'].unique():
    well_wlbStatus.append({'label':str(op),'value':op})

wlbContent_options = []
for op in explo_df['wlbContent'].unique():
    wlbContent_options.append({'label':str(op),'value':op})

    
wlbSubSea_options  = []
for op in explo_df['wlbSubSea'].unique():
    wlbSubSea_options.append({'label':str(op),'value':op})


color_options  = []
for op in ['wlbSubSea','wlbDrillingOperator','wlbPurpose','wlbStatus','wlbContent','wlbWellType','wlbTotalDepth']:
    color_options.append({'label':str(op),'value':op})

 ######    ######    ######    ######    ######    ######    ######   
dev_df = pd.read_csv('npd_overall/wellbore_development_all.csv')
well_operator_options_d = []
for op_d in dev_df['wlbDrillingOperator'].unique():
    well_operator_options_d.append({'label':str(op_d),'value':op_d})
    
well_wlbPurpose_d = []
for op_d in dev_df['wlbPurpose'].unique():
    well_wlbPurpose_d.append({'label':str(op_d),'value':op_d})

well_wlbStatus_d = []
for op_d in dev_df['wlbStatus'].unique():
    well_wlbStatus_d.append({'label':str(op_d),'value':op_d})

wlbContent_options_d = []
for op_d in dev_df['wlbContent'].unique():
    wlbContent_options_d.append({'label':str(op_d),'value':op_d})
    
wlbSubSea_options_d  = []
for op_d in dev_df['wlbSubSea'].unique():
    wlbSubSea_options_d.append({'label':str(op_d),'value':op_d})


filter_layout = dbc.Container([
            html.H4('Exploration and Development Wells in NCS'),

            dbc.Row([dbc.Col([dbc.Button("Sync data", id="example-button",size="sm" ,className="me-2", n_clicks=0,color="success"),
            dbc.Input(placeholder="Search Well or Field", type="text", id='search_input',style={"width": '330px'}),
            #html.Br(),
            dbc.Input(placeholder="latitude", type="number", id='input_lat',style={"width": '330px'}),
            #html.Br(),
            dbc.Input(placeholder="longitude", type="number", id='input_long',style={"width": '330px'}),
            #html.Br(),
            dbc.Input(placeholder="radius", type="number", id='input_rad',style={"width":'330px'})])]),
            html.Br(),
            
        
            
                    dbc.Row([dbc.Col([        html.H6('Filter Data:'),
                            html.Br(),
                            dcc.Dropdown(id='Field_Names',
                                        options=field_options
                                        ,placeholder='Field Name'
                                        ,multi=True, style={'width': '330px'}),
                            #html.Br(),

                           dcc.Dropdown(id='Well_type',
                                        options=well_type_options
                                        ,placeholder='Well Type'
                                        ,multi=True, style={'width': '330px'}),
                           # html.Br(),
                            dcc.Dropdown(id='Operatorr',
                                        options=well_operator_options_ex
                                        ,placeholder='Operator'
                                        ,multi=True, style={'width': '330px'}),
                        
                           # html.Br(),
                           dcc.Dropdown(id='Purposer',
                                        options=well_wlbPurpose
                                        ,placeholder='Purpose'
                                        ,multi=True, style={'width': '330px'}),
                            dcc.Dropdown(id='Statusr',
                                        options=well_wlbStatus
                                        ,placeholder='Status'
                                        ,multi=True, style={'width': '330px'}),
                            dcc.Dropdown(id='Contentr',
                                        options=wlbContent_options
                                        ,placeholder='Content'
                                        ,multi=True, style={'width': '330px'}),
                            dcc.Dropdown(id='SubSear',
                                        options=wlbSubSea_options
                                        ,placeholder='Subsea'
                                        ,multi=True, style={'width': '330px'}),
                            
                            dcc.Dropdown(id='Color_Optionr',
                                        options=color_options
                                        ,placeholder='Color Option'
                                        ,multi=True, style={'width': '330px'}),
            
            
        html.Div([html.Button(id='My_button', 
                            n_clicks=0, 
                            children='Display', 
                            style={'fontSize':20,'display':'inline-block'}),
                    
                    html.Output(id='text_out')
                    ])
                    ])])])
                    
                   # ],body=True ,color="light"),className="mt-3

