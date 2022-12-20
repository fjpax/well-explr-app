import dash
from dash import Input, Output, State, html, Dash, callback, dcc,dash_table
import dash_bootstrap_components as dbc

import os
# Import necessary libraries 

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

from npd_overall.utils.in_radius import if_in_distance                                                                                                           

import pickle
###########
dash.register_page(__name__,path='/pages/overview-pages/overview-table-pages')

from pages.filter_all_table_only import filter_layout_table
#######
###########

#   









######
######







table_columns = ['wlbWellboreName', 'wlbEntryDate','wlbDrillingOperator','wlbTotalDepth',
                'wlbProductionLicence', 'wlbPurpose', 'wlbStatus', 'wlbContent',
                'wlbWellType',  'wlbNsDecDeg', 'wlbEwDesDeg']
edited_columns = ['Wellbore Name', 'Entry Date','Drilling Operator','Total Depth (MD)[m RKB]',
                'Production Licence', 'Purpose', 'Status', 'Content',
                'Well Type',  'Ns Deg', 'Ew Deg']
new_names_of_columns = dict(zip(table_columns,edited_columns))
layout = dbc.Container(
    [dbc.Row([
                dbc.Button(
                    "Show Filter",
                    id="table_only_overview_button",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    filter_layout_table,
                    id="collapse_table_only_overview",
                    is_open=False,
                  
                    style= {"background-color": "DarkGrey"}
                )]),

        html.Hr(),
        dcc.Store(id='memory-output_table_only'),
        dbc.Row([dash_table.DataTable(
                        id='table_only_overview',
                        columns=[
                        {"name": i, "id": i} for i in edited_columns
                            ],

                      
                        style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },

                        style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['wlbWellboreName', 'wlbEntryDate']
                            ],

                        page_current=0,
                        page_size=30,
                        page_action='custom',



                        filter_action='custom',
                        filter_query='',
                        sort_action='custom',
                        sort_mode='multi',
                        sort_by=[]
                        
                        )],
                        style={  'height': 1100, 'overflowY': 'scroll'},
                        #className='six columns'
                                             
                        align="center",)],
                        
    fluid=True,style={'marginBottom': 100})




operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part_table_only(filter_part):
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


#table############
##################
@callback(Output('table_only_overview', "data"),
            Input('memory-output_table_only','data'),
            Input('table_only_overview', "page_current"),
           Input('table_only_overview', "page_size"),
           Input('table_only_overview', "sort_by"),
             Input('table_only_overview', "filter_query")
)

def plot_output_table_only(filtered_well_data,page_current, page_size, sort_by, filter):

    print('hello6')
    dff = pd.DataFrame.from_dict(filtered_well_data)
    dff= dff.rename(columns=new_names_of_columns)
    
    filtering_expressions = filter.split(' && ')
    
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part_table_only(filter_part)

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
    

    #print(dff)
    return dff.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records')

# ###############
# #filter data
# ##############
@callback(Output('memory-output_table_only', "data"),
             Input('My_button_table_only','n_clicks'),
             [State('Field_Names_table_only','value'),
             State('Well_type_table_only','value'),
             State('Operatorr_table_only','value'),
             State('Purposer_table_only','value'),
             State('Statusr_table_only','value'),
             State('Contentr_table_only','value'),
             State('SubSear_table_only','value'),
             State('Color_Optionr_table_only','value'),
             State('search_input_table_only','value'),
             State('input_lat_table_only','value'),
             State('input_long_table_only','value'),
             State('input_rad_table_only','value'),
             State('table_only_overview', "sort_by"),
             State('table_only_overview', "filter_query")
            ])

def plot_data_overview_table_only(n_clicks,Field_Name_ss, Well_type_chosen, Operatorss, Purposes, Statuss,Contents,Subseas,Color_Optionss,search_input_text, lat1, lon1,radius, sort_by, filter):#,Sizes,Colors):
    print('hello1')
    well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')
    print('hello1')
    filtered_well_data = well_data_orig.copy()

#     ###load field wells dict
    field_wells_with_explo_and_dev_dict= pickle.load(open("npd_overall/field_wells_with_explo_and_dev_dict.pkl", "rb"))
    print('hello2')
#     ###
    if Field_Name_ss:
                field_wells=[]
                field_wells.append(field_wells_with_explo_and_dev_dict[Field_Name_ss[0]]['exploration'])
                field_wells.append(field_wells_with_explo_and_dev_dict[Field_Name_ss[0]]['development'])
                field_wells = [item for sublist in field_wells for item in sublist]
                filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(field_wells)]
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
            
    if search_input_text:
        if search_input_text in list(filtered_well_data['wlbWellboreName']):
            filtered_well_data = filtered_well_data[filtered_well_data['wlbWellboreName']==search_input_text]  

        else:
            field_wells=[]
            field_wells.append(field_wells_with_explo_and_dev_dict[search_input_text]['exploration'])
            field_wells.append(field_wells_with_explo_and_dev_dict[search_input_text]['development'])
            field_wells = [item for sublist in field_wells for item in sublist]
            filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(field_wells)]
            print('num:fieldwelss:', len(field_wells))
          
    if lat1:
        well_chosen = if_in_distance(radius, lon1,lat1)
        filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(well_chosen)]
     
    if not Color_Optionss:
        Color_Optionss =['wlbContent']
    print('hello3')
    ###############
    #table#########
    ###############
    dff = filtered_well_data[table_columns]
    


    return dff.to_dict('records')

#####################
#collapse toggle
#######################

@callback(
    Output("collapse_table_only_overview", "is_open"),
    [Input("table_only_overview_button", "n_clicks")],
    [State("collapse_table_only_overview", "is_open")],
)
def toggle_collapse_table_only(n, is_open):
    print('from toggle!')
    if n:
        return not is_open
    return is_open
