import dash
from dash import Input, Output, State, html, Dash, callback, dcc,dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import os
# Import necessary libraries 
from utils.viz_wellpath import viz_wellpath_plot

import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
#from plotly.subplots import make_subplots
#import json
#import numpy as np
#%config Completer.use_jedi = False
import dash_bootstrap_components as dbc
import json
from datetime import datetime
from flask_caching import Cache
#import fiona
import geojson

import geopandas as gpd

import plotly.graph_objects as go
from npd_overall.utils.in_radius import if_in_distance                                                                                                           
from npd_overall.utils.subplot_casingProf import subplot_well_profile
from npd_overall.utils.subplot_casingProf import plot_casing_and_statigraphy_3D
import pickle
###########


#dash.register_page(__name__)


###########


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







#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],prevent_initial_callbacks=False)#, prevent_initial_callbacks=False)

# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory'
# })

# TIMEOUT = 1000

# @cache.memoize(timeout=TIMEOUT)
# def query_data():
#     f = open('npd_overall/NEWactive_license.json' ,'r+', encoding="utf-8")
#     gj = geojson.load(f)
#         #geodatadf
#     df = pd.read_csv('processedActiveGeoDF.csv')
        
#         #layer for licences

#     figdf = px.choropleth_mapbox(df, geojson=gj, locations='prlName', hover_name="cmpLongName",
#                             #color="cmpLongName",
#                             #  color_continuous_scale="Viridis",
#                             #range_color=(0, 12),
#                             mapbox_style="carto-positron",
#                             #zoom=2, center = {"lat": well_data["wlbNsDecDeg"].mean()+5, "lon": well_data["wlbEwDesDeg"].mean()+5},
#                             #zoom=2, center = {"lat": 65.7, "lon": 9},
#                             featureidkey="properties.prlName",
#                             opacity=0.3,
#                             labels={'unemp':"cmpLongName"}
#                             )
#     return figdf

# def dataframe():
#     return query_data()



controls_1 = dbc.Card([
        dbc.Row([html.H4('Exploration and Development Wells in NCS')]),

        dbc.Button("Sync data", id="example-button",size="sm" ,className="me-2", n_clicks=0,color="success"),

        #dbc.Button("Search", id='searh-button', size='sm',n_clicks=0,className="me-3"),

        dbc.Row([dbc.Input(placeholder="Search Well or Field", type="text", id='search_input',style={"width": 200})]),
        dbc.Row([dbc.Input(placeholder="latitude", type="number", id='input_lat',style={"width": 200})]),
        dbc.Row([dbc.Input(placeholder="longitude", type="number", id='input_long',style={"width": 200})]),
        dbc.Row([dbc.Input(placeholder="radius", type="number", id='input_rad',style={"width": 200})]),

        
        
        dbc.Row([html.H6('Filter Data:')]),

        dbc.Row([ dcc.Dropdown(id='Field_Names',
                    options=field_options
                    ,placeholder='Field Name'
                    ,multi=True, style={'width': '370px'})]),


       dbc.Row([ dcc.Dropdown(id='Well_type',
                    options=well_type_options
                    ,placeholder='Well Type'
                    ,multi=True, style={'width': '370px'})]),
        
       dbc.Row([ dcc.Dropdown(id='Operatorr',
                    options=well_operator_options_ex
                    ,placeholder='Operator'
                    ,multi=True, style={'width': '370px'})]),
    
    
        dbc.Row([dcc.Dropdown(id='Purposer',
                    options=well_wlbPurpose
                    ,placeholder='Purpose'
                    ,multi=True, style={'width': '370px'})]),
        dbc.Row([dcc.Dropdown(id='Statusr',
                    options=well_wlbStatus
                    ,placeholder='Status'
                    ,multi=True, style={'width': '370px'})]),
        dbc.Row([dcc.Dropdown(id='Contentr',
                    options=wlbContent_options
                    ,placeholder='Content'
                    ,multi=True, style={'width': '370px'})]),
       dbc.Row([ dcc.Dropdown(id='SubSear',
                    options=wlbSubSea_options
                    ,placeholder='Subsea'
                    ,multi=True, style={'width': '370px'})]),
        
        dbc.Row([ dcc.Dropdown(id='Color_Optionr',
                    options=color_options
                    ,placeholder='Color Option'
                    ,multi=True, style={'width': '370px'})]),
        
        
       dbc.Row([ html.Div([html.Button(id='My_button', 
                        n_clicks=0, 
                        children='Display', 
                        style={'fontSize':20,'display':'inline-block'}),
                  
                  html.Output(id='text_out')
                 ])])],

            body=True ,color="light")



table_columns = ['wlbWellboreName', 'wlbDrillingOperator','wlbTotalDepth']
#,'wlbContent','wlbPurpose','wlbWellType', 'wlbStatus', 'wlbEntryDate','wlbProductionLicence',  'wlbNsDecDeg', 'wlbEwDesDeg','wlbSubSea']

layout = dbc.Container(
    [   html.Br(),
        html.Br(),
        html.H1('Norwegian Continental Shelf Dashboard'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_1, md=4),
                dbc.Col(dcc.Graph(id='My_plot'), md=8),
            ],
            align="center"
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                
                dbc.Col(dcc.Graph(id='My_sub_plot')),
            ],
            align="center",
        ),
        dbc.Row([
            html.Div([
                dash_table.DataTable(
                    id='table-overview',
                    columns=[
                        {"name": i, "id": i} for i in table_columns
                    ],
                    page_current=0,
                    page_size=20,
                    page_action='custom',#'custom',


                   # editable=True,

                    column_selectable="multi",
                    row_selectable="multi",
                
                    filter_action='custom',#'custom',
                    filter_query='',

                    sort_action='custom',#'custom',
                    sort_mode='multi',
                    sort_by=[]
                )],
                style={  'height': 750, 'overflowY': 'scroll'},
                #className='six columns'
            )],
                align="center",
            ),

        #     dbc.Row(
        #     [
                
        #         dbc.Col(dcc.Graph(id='My_sub_plot2')),
        #     ],
        #     align="center",
        # ),


       
    ],
    fluid=True,style={'marginBottom': 100}
)
 




operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3



##################################################
####first callback for explo wells########
##################################################
@callback([Output('My_plot','figure'),
            Output('table-overview', "data")],
             [Input('My_button','n_clicks')],
             [State('Field_Names','value'),
             State('Well_type','value'),
             State('Operatorr','value'),
             State('Purposer','value'),
             State('Statusr','value'),
             State('Contentr','value'),
             State('SubSear','value'),
             State('Color_Optionr','value'),
             State('search_input','value'),
             State('input_lat','value'),
             State('input_long','value'),
             State('input_rad','value'),
             
            State('table-overview', "page_current"),
            State('table-overview', "page_size"),
            State('table-overview', "sort_by"),
            State('table-overview', "filter_query")
            ])#,
           # State('Sizer','value'),
           #   State('Colorr','value')])

def plot_data_overview(n_clicks,Field_Name_ss, Well_type_chosen, Operatorss, Purposes, Statuss,Contents,Subseas,Color_Optionss,search_input_text, lat1, lon1,radius,page_current, page_size, sort_by, filter):#,Sizes,Colors):
    well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')
   
    filtered_well_data = well_data_orig.copy()

    ###load field wells dict
    field_wells_with_explo_and_dev_dict= pickle.load(open("npd_overall/field_wells_with_explo_and_dev_dict.pkl", "rb"))
    zoom=2
    ###
    if Field_Name_ss:
                field_wells=[]
                field_wells.append(field_wells_with_explo_and_dev_dict[Field_Name_ss[0]]['exploration'])
                field_wells.append(field_wells_with_explo_and_dev_dict[Field_Name_ss[0]]['development'])
                field_wells = [item for sublist in field_wells for item in sublist]
                filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(field_wells)]
                zoom=8

    if Well_type_chosen:
                
                filtered_well_data = filtered_well_data[filtered_well_data.wlbWellType.isin(Well_type_chosen)]
                
                
    if Operatorss:
                filtered_well_data = filtered_well_data[filtered_well_data.wlbDrillingOperator.isin(Operatorss)]
        
    if Purposes:
                filtered_well_data = filtered_well_data[filtered_well_data.wlbPurpose.isin(Purposes)]   
            
    if Statuss:
                filtered_well_data = filtered_well_data[filtered_well_data.wlbStatus.isin(Statuss)]
            
    if Contents:
                filtered_well_data = filtered_well_data[filtered_well_data.wlbContent.isin(Contents)]
            
    if Subseas:
                filtered_well_data = filtered_well_data[filtered_well_data.wlbSubSea.isin(Subseas)]
            
    marker_size=None

    

    if search_input_text:
        if search_input_text in list(filtered_well_data['wlbWellboreName']):
            filtered_well_data = filtered_well_data[filtered_well_data['wlbWellboreName']==search_input_text]  
            marker_size=[18]

        else:
            field_wells=[]
           
            field_wells.append(field_wells_with_explo_and_dev_dict[search_input_text]['exploration'])
            field_wells.append(field_wells_with_explo_and_dev_dict[search_input_text]['development'])
            field_wells = [item for sublist in field_wells for item in sublist]
            filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(field_wells)]
            print('num:fieldwelss:', len(field_wells))
            marker_size=None
        zoom=8
          
    if lat1:
        well_chosen = if_in_distance(radius, lon1,lat1)
        filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(well_chosen)]
        marker_size=None
        zoom=7

    
      
    
    
   
    ##geojson
    startTime = datetime.now()

    infile = open('/Users/2924441/Desktop/phd part 2/add_fm_data/npd_overall/active_licenses_figure.pkl','rb')
    active_licenses_figure = pickle.load(infile)
    #fig1 = dataframe()
    fig1 = active_licenses_figure 
    print(type(fig1))    
    print('cpboxmap:',datetime.now() - startTime)

    if not Color_Optionss:
        Color_Optionss =['wlbContent']
  
    startTime = datetime.now()
    ################# Exploration Wells
    fig = px.scatter_mapbox(filtered_well_data, lat="wlbNsDecDeg", lon="wlbEwDesDeg", custom_data=["wlbWellboreName"], hover_name="wlbDrillingOperator", hover_data=["wlbWellboreName", "wlbPurpose"],
            color=Color_Optionss[0], height=500, width = 600, size=marker_size)
    #fig.update_layout(mapbox_style="open-street-map")

    fig1.add_traces([shows for shows in fig.data[:]])
    
    #######

   

    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})#)  , zoom=2, center = {"lat": filtered_well_data["wlbNsDecDeg"].mean()+5, "lon": filtered_well_data["wlbEwDesDeg"].mean()+5})
    fig1.update_mapboxes(zoom=zoom, center = {"lat": filtered_well_data["wlbNsDecDeg"].mean(), "lon": filtered_well_data["wlbEwDesDeg"].mean()})
    print('center:',filtered_well_data["wlbNsDecDeg"].mean())
    print('scatter:',datetime.now() - startTime)


    ###############
    #table##############
    ###############
    dff = filtered_well_data[table_columns]
    filtering_expressions = filter.split(' && ')
    
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    
    return [fig1,   dff.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')]


######################
@callback(
    Output('My_sub_plot', 'figure'),
    [Input('My_plot', 'selectedData')])
    
def callback_data_overview(selectedData):
  
    well_list_chosen=[]
    for curve in selectedData.get('points'):
        if 'customdata' in curve.keys():
            well_list_chosen.append(curve['customdata'][0])

    well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')      
    list1_as_set = set(well_data_orig[well_data_orig['wlbWellType']=='EXPLORATION']['wlbWellboreName']) 
    well_list_chosen = list1_as_set.intersection(well_list_chosen)

    #well_list_chosen = ['1/2-1','1/2-2','8/1-1','30/9-19 A','8/1-1','1/2-1','8/1-1']
    fig_data_list_all, stratigraphy_data_list_all = plot_casing_and_statigraphy_3D(well_list_chosen,stratigraphy_all_dict,well_casing_design_all_dict)
    fig = subplot_well_profile(fig_data_list_all, stratigraphy_data_list_all)
    
    
    return fig


