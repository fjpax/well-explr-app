import dash
from dash import Input, Output, State, html, Dash, callback, dcc,dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import json
import geojson
from datetime import datetime
from npd_overall.utils.in_radius import if_in_distance
from npd_overall.utils.subplot_casingProf import subplot_well_profile
from npd_overall.utils.subplot_casingProf import plot_casing_and_statigraphy_3D
import pickle

from dash import no_update
import requests
import os
global URL, HEADERS

URL = os.environ.get("bot_url")
HEADERS = {
    'X-Api-Key': os.environ.get("X-Api-Key"),
    'Content-Type': 'application/json'
}


from bot_assistant.utils import run_conversation, message_appender

###########
from pages.filter_all import filter_layout
dash.register_page(__name__)





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







def npd_sun(df):
    fig = px.sunburst(df, path=  ['wlbWellType', 'wlbContent','wlbPurpose', 'wlbStatus','wlbDrillingOperator'])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(textinfo="label+percent parent")

    return fig



table_columns = ['wlbWellboreName', 'wlbDrillingOperator','wlbTotalDepth']
#,'wlbContent','wlbPurpose','wlbWellType', 'wlbStatus', 'wlbEntryDate','wlbProductionLicence',  'wlbNsDecDeg', 'wlbEwDesDeg','wlbSubSea']


layout = dbc.Container(
    [  dbc.Row([
                dbc.Button(
                    "Show Filter",
                    id="collapse_button_drilling_filter_all",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    filter_layout,
                    id="collapse_drilling_filter_all",
                    is_open=False,
                  
                  #  style= {"background-color": "DarkGrey"}
                )]),

        html.Hr(),
        dcc.Store(id='overview-dropdown-store'),
        dbc.Row([  dbc.Col([
                        html.H1('Chatbot Assistant'),
                        dcc.Store(id='conversation-list-store'),
                        dcc.Store(id='function-call-store'),
                        dcc.Store(id='time-store'),
                        dcc.Store(id='time-dropdown-store'),
                        dcc.Textarea(id='conversation', value='', readOnly=True, style={'width': '100%', 'height': '60vh'}),
                        html.Div([
                            dcc.Input(id='input-field', type='text', placeholder='Type your message...', style={'width': '80%', 'height': '10vh'}),
                            html.Button('Send', id='send-button', n_clicks=0, style={'marginLeft': '10px','height': '10vh' })
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ], style={'width': '400px', 'margin': 'auto'}),
                    
                    dbc.Col(dcc.Graph(id='My_plot',style={  'height': '80vh'}) ,width = 6),#, md=8),

                    dbc.Col([
                          dbc.Row([html.H3('Summary'),
                                    dcc.Graph(id='My_plot_sun_npd',style={'height': '40vh'})]),

                          dbc.Row([#dbc.NavLink("Expand Table", href=dash.page_registry['pages.overview_pages.overview_table_pages']['path']),
                                   dcc.Link("Expand Table", href='/pages/overview-pages/overview-table-pages'),
                                    
                                    dash_table.DataTable(
                                            id='table-overview',
                                            columns=[
                                                {"name": i, "id": i} for i in table_columns
                                            ],
                                            page_current=0,
                                            page_size=9,
                                            page_action='custom',#'custom',
                                            # editable=True,

                                            column_selectable="multi",
                                            row_selectable="multi",
                                        
                                            filter_action='custom',#'custom',
                                            filter_query='',

                                            sort_action='custom',#'custom',
                                            sort_mode='multi',
                                            sort_by=[]
                                                 )
                                    ],
                                        style={  'height': '40vh', 'overflowY': 'scroll'},#750
                                        #className='six columns'
                                             
                                        align="center",
                                            ),

                        ],width = 4,style={  'height': '80vh'}),
              ],
            #align="center",
            #className="g-0" 
             ),

        
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



@callback(
    [Output('conversation', 'value'), 
     Output('input-field', 'value'), 
     Output('conversation-list-store', 'data'), 
     Output('function-call-store', 'data'),
     Output('time-store', 'data')],

    [Input('send-button', 'n_clicks')],

    [State('input-field', 'value'), 
     State('conversation', 'value'), 
     State('conversation-list-store', 'data')]
)
def update_conversation(n_clicks, message, conversation, conversation_list):
    if n_clicks > 0:
        # Append the user's message to the conversation
        current_query = {"role": "user", "content": message}
        
        print('n_clicks: ',n_clicks)
        #if conversation is already ongoing
        if n_clicks > 1 :
            conversation_list = message_appender(conversation_list,current_query)

        #if conversation is starting
        else:
            #Variables:
            prompt_message = [{"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}]
            conversation_list= []
            conversation_list = message_appender(prompt_message, current_query)

        current_resposonse = run_conversation(conversation_list)
        conversation_list = message_appender(conversation_list, {"role": "assistant", "content":str(current_resposonse['json_response'])})

        #check if current response has a function_name key
        try: 
            #check if current response has a function_name key
            if current_resposonse['function_name']=='plot_the_overview_of_the_norwegian_sea':
                print('with update: plot_the_overview_of_the_norwegian_sea')
                conversation += f'User: {message}\n'
                overview_param = current_resposonse['json_response']
                # Process the user's message and generate a response
                response = 'Bot: \n' + str(overview_param)
                # Append the bot's response to the conversation
                conversation += response
                    
                #load the well data
                well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')
                filtered_well_data = well_data_orig.copy()
                ###load field wells dict
                field_wells_with_explo_and_dev_dict= pickle.load(open("npd_overall/field_wells_with_explo_and_dev_dict.pkl", "rb"))
                zoom=3

                Field_Name_ss = overview_param.get('Field_Name', None)
                Well_type_chosen = overview_param.get('Well_type', None)
                Operatorss = overview_param.get('Operator', None)
                Purposes = overview_param.get('Purpose', None)
                Statuss = overview_param.get('Status', None)
                Contents = overview_param.get('Content', None)
                Subseas = None
                lat1 = overview_param.get('latitude', None)
                lon1 = overview_param.get('longitude', None)
                radius = overview_param.get('radius', None)
                well_names_user = overview_param.get('well_names', None)
                search_input_text = None
                Color_Optionss = None
                sort_by = []
                filter = ""

                ###
                if Field_Name_ss:
                            print(filtered_well_data.shape, '///1')
                            print('field_name_ss:',Field_Name_ss)
                            field_wells=[]
                            field_wells.append(field_wells_with_explo_and_dev_dict[Field_Name_ss[0]]['exploration'])
                            field_wells.append(field_wells_with_explo_and_dev_dict[Field_Name_ss[0]]['development'])
                            field_wells = [item for sublist in field_wells for item in sublist]
                            filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(field_wells)]
                            zoom=8
                print(filtered_well_data.shape, '///2')
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

                
                if well_names_user:
                    #filter the filtered_well_data column wellborename with the well_names_user elements
                    filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(well_names_user)]
                    marker_size=[18]
                    
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

            
                return conversation, '' , conversation_list, filtered_well_data.to_dict('records'), {'created' :datetime.now(), 'zoom': zoom}
            
            if current_resposonse['function_name']=='plot_the_wells_on_map_based_on_radius_latitutde_longitude':
                print('with update: plot_the_wells_on_map_based_on_proximity')
                conversation += f'User: {message}\n'
                overview_param = current_resposonse['json_response']
                print('overview_param:',overview_param)
                # Process the user's message and generate a response
                response = 'Bot: \n' + str(overview_param)
                # Append the bot's response to the conversation
                conversation += response

                #load the well data
                well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')
                filtered_well_data = well_data_orig.copy()

                well_names_user = overview_param.get('well_names', None)
                lat1 = overview_param.get('latitude', None)
                lon1 = overview_param.get('longitude', None)
                radius = overview_param.get('radius', None)
                
                #if lat1 or lon1 are not available but well_names_user is available, then get the lat and lon of the single well from the filtered well data
                if not lat1 or not lon1:
                    if well_names_user:
                        lat1 = filtered_well_data[filtered_well_data['wlbWellboreName']==well_names_user[0]]['wlbNsDecDeg'].values[0]
                        lon1 = filtered_well_data[filtered_well_data['wlbWellboreName']==well_names_user[0]]['wlbEwDesDeg'].values[0]
                        zoom = 8
                #if lat1, lon1 and radius are available, then get the well names in the radius
                if lat1 and lon1:
                    well_chosen = if_in_distance(radius, lon1,lat1)
                    #include the well_names_user in the well_chosen
                    if well_names_user:
                        well_chosen.append(well_names_user)
                    filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(well_chosen)]
                    marker_size=None
                    zoom=7

                
                return conversation, '' , conversation_list, filtered_well_data.to_dict('records'), {'created' :datetime.now(), 'zoom':zoom}#overview_param
            
            if current_resposonse['function_name']=='get_answer_to_question':
                print('with no update: answer_the_question')
                max_attempts = 2
                attempt = 0
                conversation += f'User: {message}\n'

                while attempt < max_attempts:
                    response = requests.post(URL, headers=HEADERS, data=json.dumps({"message": message}))
                    
                    if response.status_code == 504:  # Gateway Timeout
                        print(f'Response 504 (Gateway Timeout), retrying... (attempt {attempt+1})')
                        attempt += 1
                    else:
                        # continuation of normal execution, process the response...
                        # Process the user's message and generate a response
                        response = 'Bot: \n' + str(json.loads(response.text)['chat_response']['answer']['message'])
                        break  
                    
                    if attempt == max_attempts:
                        print(f'Request failed after {attempt} attempts due to repeated 504 responses')
                        response = 'Request failed after {attempt} attempts due to repeated 504 responses'

                # Append the bot's response to the conversation
                conversation += response

                return conversation, '' , conversation_list, no_update, no_update
            
        except KeyError:
            conversation += f'User: {message}\n'
            # Process the user's message and generate a response
            response = 'Bot: \n' + str(current_resposonse['json_response']['content'])
            # Append the bot's response to the conversation
            conversation += response
            print('with no update 1')
            return conversation, '' , conversation_list, no_update, no_update

        except Exception as e:
            # Handle other unexpected exceptions
            # You might want to log the exception message for debugging purposes
            print(f"An unexpected error occurred: {e}")
            
    return conversation, None, conversation_list,no_update , no_update

##################################################
#####table callback########
##################################################
@callback(Output('table-overview', "data"),
            Input('overview-dropdown-store','data'),
            Input('table-overview', "page_current"),
           Input('table-overview', "page_size"),
)

def plot_output(filtered_well_data,page_current, page_size):
  
    dff = pd.DataFrame.from_dict(filtered_well_data)
 
    return dff.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records')



###callback from the click old option, the dropdown option and the search input
@callback([Output('overview-dropdown-store', "data"),Output('time-dropdown-store', "data")],
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
             State('table-overview', "sort_by"),
             State('table-overview', "filter_query")
            ])
def drop_down_overview_filtered_data(n_clicks,Field_Name_ss, Well_type_chosen, Operatorss, Purposes, Statuss,Contents,Subseas,Color_Optionss, search_input_text, lat1,lon1,radius,sort_by,filter):
    """callback for generating dataframe from the dropdowns overview page

    :param _type_ n_clicks: _description_
    :param _type_ Field_Name_ss: _description_
    :param _type_ Well_type_chosen: _description_
    :param _type_ Operatorss: _description_
    :param _type_ Purposes: _description_
    :param _type_ Statuss: _description_
    :param _type_ Contents: _description_
    :param _type_ Subseas: _description_
    :param _type_ Color_Optionss: _description_
    :param _type_ search_input_text: _description_
    :param _type_ lat1: _description_
    :param _type_ lon1: _description_
    :param _type_ radius: _description_
    :param _type_ sort_by: _description_
    :param _type_ filter: _description_
    :return _type_: _description_
    """

    well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')
   
    filtered_well_data = well_data_orig.copy()

    ###load field wells dict
    field_wells_with_explo_and_dev_dict= pickle.load(open("npd_overall/field_wells_with_explo_and_dev_dict.pkl", "rb"))
    zoom=3
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
     
            marker_size=None
        zoom=8
          
    if lat1:
        well_chosen = if_in_distance(radius, lon1,lat1)
        filtered_well_data = filtered_well_data[filtered_well_data.wlbWellboreName.isin(well_chosen)]
        marker_size=None
        zoom=7

    return [filtered_well_data.to_dict('records'), {'created' :datetime.now(), 'zoom': zoom}]




##################################################
####first callback for explo wells########
##################################################
@callback([
            Output('My_plot','figure'),
            Output('My_plot_sun_npd','figure')],
             [Input('overview-dropdown-store','data'),
              Input('function-call-store','data')],
             [
             State('table-overview', "sort_by"),
             State('table-overview', "filter_query"),
             State('time-store','data'),
             State('time-dropdown-store','data')
             ,
            ])#,
           # State('Sizer','value'),
           #   State('Colorr','value')])

def plot_data_overview(memory_output, function_call_store, sort_by, filter, time_funccall_store, time_dropdown_store):#,Sizes,Colors):#n_clicks,
    """callback for generating the map and sunburst figure when dcc.stores are updated

    :param _type_ memory_output: _description_
    :param _type_ Sizes: _description_
    :param _type_ Colors: _description_
    :raises dash.exceptions.PreventUpdate: _description_
    :return _type_: _description_
    """

    zoom=3
    #check if time store is more recent than time dropdown store
    if time_funccall_store and time_dropdown_store:
        # Compare times and return the corresponding value
        filtered_well_data = function_call_store if time_funccall_store.get('created', None) >=  time_dropdown_store.get('created', None) else memory_output
        zoom = time_funccall_store.get('zoom', 3)
    elif time_dropdown_store:
        filtered_well_data = memory_output
        zoom = time_dropdown_store.get('zoom', 3)
    elif time_funccall_store:
        filtered_well_data =  function_call_store
        zoom = time_funccall_store.get('zoom', 3)
    else:
        #raise eror saying error with time, break the process
        print('error with time')
        raise dash.exceptions.PreventUpdate
    print('zoom:',zoom)
    filtered_well_data = pd.DataFrame.from_dict(filtered_well_data)
   
    marker_size=None
   
    ##geojson
    startTime = datetime.now()

    infile = open('npd_overall/active_licenses_figure.pkl','rb')
    active_licenses_figure = pickle.load(infile)
    fig1 = active_licenses_figure 
    #print('cpboxmap:',datetime.now() - startTime)

    # if not Color_Optionss:
    Color_Optionss =['wlbContent']
  
    startTime = datetime.now()
    print(filtered_well_data.shape, 'filtered_well_data.shape')
    ################# Exploration Wells
    fig = px.scatter_mapbox(filtered_well_data, lat="wlbNsDecDeg", lon="wlbEwDesDeg", custom_data=["wlbWellboreName"], hover_name="wlbDrillingOperator", hover_data=["wlbWellboreName", "wlbPurpose"],
            color=Color_Optionss[0], size=marker_size)#height=600, width =800, 
    #fig.update_layout(mapbox_style="open-street-map")

    fig1.add_traces([shows for shows in fig.data[:]])
    
    #######

    # print(filtered_well_data["wlbNsDecDeg"].mean())
    # print(filtered_well_data["wlbEwDesDeg"].mean())
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                       legend=dict(
                        x=0.85,
                        y=1,
                        traceorder='normal',
                        font=dict(
                        size=12)))#)  , zoom=2, center = {"lat": filtered_well_data["wlbNsDecDeg"].mean()+5, "lon": filtered_well_data["wlbEwDesDeg"].mean()+5})
    fig1.update_mapboxes(zoom=zoom, center = {"lat": filtered_well_data["wlbNsDecDeg"].mean(), "lon": filtered_well_data["wlbEwDesDeg"].mean()})
    # print('center:',filtered_well_data["wlbNsDecDeg"].mean())

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
    

    return [fig1,npd_sun(filtered_well_data)]

######################
# @callback(
#     Output('My_sub_plot', 'figure'),
#     [Input('My_plot', 'selectedData')])
    
# def callback_data_overview(selectedData):
  
#     well_list_chosen=[]
#     for curve in selectedData.get('points'):
#         if 'customdata' in curve.keys():
#             well_list_chosen.append(curve['customdata'][0])

#     well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')      
#     list1_as_set = set(well_data_orig[well_data_orig['wlbWellType']=='EXPLORATION']['wlbWellboreName']) 
#     well_list_chosen = list1_as_set.intersection(well_list_chosen)

#     #well_list_chosen = ['1/2-1','1/2-2','8/1-1','30/9-19 A','8/1-1','1/2-1','8/1-1']
#     fig_data_list_all, stratigraphy_data_list_all = plot_casing_and_statigraphy_3D(well_list_chosen,stratigraphy_all_dict,well_casing_design_all_dict)
#     fig = subplot_well_profile(fig_data_list_all, stratigraphy_data_list_all)
    
    
#     return fig



@callback(
    Output("collapse_drilling_filter_all", "is_open"),
    [Input("collapse_button_drilling_filter_all", "n_clicks")],
    [State("collapse_drilling_filter_all", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
