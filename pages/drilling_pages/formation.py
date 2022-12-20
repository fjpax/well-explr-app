from dash import Dash, dash_table, dcc, html, callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

import dash
from collections import deque
dash.register_page(__name__)

import os
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# drilling_data = pd.read_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_with_fm_csv/25_4-K-7 AY1H.csv',sep=',',dtype={'hole_size': float,'Well_name':str}) 
       
# drilling_data = drilling_data.groupby(['Well_name', 'formation'], as_index = False).agg(
#                 {'HoleDepth(m)': ['mean', 'min', 'max'],'Time Averaged ROP m/h':['mean']})
# drilling_data['MD_per_drilled_fm'] =drilling_data['HoleDepth(m)']['max'] - drilling_data['HoleDepth(m)']['min']

# res = drilling_data
# res.columns = list(map(''.join if res.columns.values[1] =='' else ' '.join, res.columns.values))
# df_initial = res


table_columns = ['Well_name', 'formation', 'Time Averaged ROP m/h mean', 'MD_per_drilled_fm', 'HoleDepth(m) min', 'HoleDepth(m) max']


from dash import html
import dash_bootstrap_components as dbc

###########
from utils.ave_ROP_Depth import viz_averop_formation
from utils.viz_formation import viz_rop_formation
#xx = os.listdir('/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_with_fm_csv')
xx = os.listdir('/Users/2924441/Desktop/phd part 2/add_fm_data/all_fm')
xx = os.listdir('/Users/2924441/Desktop/phd part 2/add_fm_data/all_fm_withoutaker')

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
        dbc.Row([dcc.Dropdown(id='Well_option_drilling_strat',
                    options=well_formation_ops
                    ,placeholder='Well_options'
                    ,value = ['15_9-F-1 C', '15_9-F-11 A', '15_9-F-15 A']
                    ,multi=True, style={'width': '370px'}),
                
                html.Div(html.Button(id='my_button_drilling_strat', 
                        n_clicks=0, 
                        children='Display', 
                        style={'fontSize':20,'display':'inline-block'})
                    ),
                html.Div([
                            html.Button("Download CSV", id="btn_csv",
                        style={'fontSize':20,'display':'inline-block'}),
                            dcc.Download(id="download-dataframe-csv")]) ,
                html.Div([
                            html.Button("API", id="api_csv",
                        style={'fontSize':20,'display':'inline-block'}),
                            dcc.Download(id="api-dataframe-csv")])   



                            ])

       
    ],
    
)







layout = html.Div(
    className="row",
    children=[
        html.Div([
            dbc.Row([
                dbc.Button(
                    "Show Filter",
                    id="collapse_button_drilling_strat",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                   
                    dropdowns,
                    
                    id="collapse_drilling_strat",
                    is_open=False,
                ),dcc.Store(id='memory-output_formations_under_drillingpage')]),
                       


                ]),

        html.Div(
            dcc.Graph(id='table-paging-with-graph-container',style={'height': '40vh'})

           
           
                    ),
        html.Div( dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in table_columns#df_initial.columns
                ],
                page_current=0,
                page_size=15,
                page_action='custom',
        
             

                filter_action='custom',
                filter_query='',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[],
                style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        }),
            style={'height': '50vh', 'overflowY': 'scroll'},
           
        ),
        
        # html.Div(dcc.Graph(id='table-paging-with-graph-container-depthROP'),
        #     className="five columns"
        # )
    ]
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


###########################################
@callback(Output('table-paging-with-graph', "data"),
            Input('memory-output_formations_under_drillingpage','data'),
            Input('table-paging-with-graph', "page_current"),
           Input('table-paging-with-graph', "page_size"),
           Input('table-paging-with-graph', "sort_by"),
             Input('table-paging-with-graph', "filter_query")
)

def plot_output_table_only(filtered_well_data,page_current, page_size, sort_by, filter):

    
    dff = pd.DataFrame.from_dict(filtered_well_data)

    
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
    

    #print(dff)
    return dff.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records')


###########################################
@callback(
    Output("collapse_drilling_strat", "is_open"),
    [Input("collapse_button_drilling_strat", "n_clicks")],
    [State("collapse_drilling_strat", "is_open")],
)
def toggle_collapse_drilling_strat(n, is_open):
    if n:
        return not is_open
    return is_open


###########################################
@callback(
    Output('memory-output_formations_under_drillingpage', "data"),
    Input('my_button_drilling_strat','n_clicks'),
    State('table-paging-with-graph', "sort_by"),
    State('table-paging-with-graph', "filter_query"),
    State('Well_option_drilling_strat', "value"))
def update_table_drilling_strat(n_clicks, sort_by, filter, well_name_chosen):
    print('tableeeeee',well_name_chosen)
    dff = pd.DataFrame()
    for well_name in  well_name_chosen:
        df = pd.read_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_with_fm_csv'+'/'+well_name+'.csv', sep=',')
        dff = pd.concat([dff, df],
                                ignore_index = True,
                                sort = False)
    dff = dff.groupby(['Well_name', 'formation'], as_index = False).agg(
                {'HoleDepth(m)': ['mean', 'min', 'max'],'Time Averaged ROP m/h':['mean']}).round(2)
    dff['MD_per_drilled_fm'] =(dff['HoleDepth(m)']['max'] - dff['HoleDepth(m)']['min']).round(2)

 
    dff.columns = list(map(lambda x: x[0] if x[1] =='' else ' '.join(x), dff.columns.values))
    
 


    dff = dff[table_columns]  
            
   

    

    return dff.to_dict('records')





###########################################

@callback(
    [Output('table-paging-with-graph-container', "figure")],
    [Input('my_button_drilling_strat','n_clicks')],
    [State('Well_option_drilling_strat', "value")],
)
def plot_data_drilling_strat(n_clicks, well_name_chosen):
   
    return [viz_averop_formation(well_name_chosen)]


###########################################

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('Well_option_drilling_strat', "value"),
    prevent_initial_call=True,
)

def func_drilling_strat(n_clicks,well_name_chosen):

    dff = pd.DataFrame()
    for well_name in  well_name_chosen:
        df = pd.read_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_with_fm_csv'+'/'+well_name+'.csv', sep=',')
        dff = pd.concat([dff, df],
                                ignore_index = True,
                                sort = False)
    dff = dff.groupby(['Well_name', 'formation'], as_index = False).agg(
                {'HoleDepth(m)': ['mean', 'min', 'max'],'Time Averaged ROP m/h':['mean']})
    dff['MD_per_drilled_fm'] =dff['HoleDepth(m)']['max'] - dff['HoleDepth(m)']['min']

 
    dff.columns = list(map(''.join if dff.columns.values[1] =='' else ' '.join, dff.columns.values))
    return dcc.send_data_frame(dff.to_csv, "mydf.csv")



# @callback(
#     [Output('table-paging-with-graph-container-depthROP', "figure")],
#     [Input('my_button_drilling_strat','n_clicks')],
#     [State('Well_option_drilling_strat', "value")],
# )

# def plot_data_drilling_strat_realtime(n_clicks, well_name_chosen):

#     return [viz_rop_formation(deque(well_name_chosen,maxlen=3))]
