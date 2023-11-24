
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio

def survey_interpolator_for_annotations(df, df_annon ,data_concat_all):
    """interpolate based on MD

    :param _type_ df: _description_
    :param _type_ df_annon: _description_
    :param _type_ data_concat_all: _description_
    :return _type_: _description_
    """
    data_concat = pd.concat([df, df_annon],
                            ignore_index = True,
                            sort = False).sort_values('MD(m RKB)')
    data_concat.interpolate(method='linear' ,inplace=True)

    data_concat_all = pd.concat([data_concat_all ,data_concat[~data_concat['Report'].isna()]],
                                ignore_index = True,
                                sort = False).sort_values('MD(m RKB)')

    return data_concat_all, data_concat


# function to create wellpath plot
def viz_wellpath_plot(well_names, show_dogleg=False,show_incidents=True):
    data = []
    x_list = []
    y_list = []
    z_list = []
    annotations = []
    data_concat_all = pd.DataFrame()
    for well_name in well_names:
        df = pd.read_csv('all_survey_csv/' + well_name + '.csv', sep=',')
        annons = True
        if annons:
            try:
                df_annon = pd.read_csv(
                    'operation_csv/' + well_name + '.csv', sep=';')
                data_concat_all, df = survey_interpolator_for_annotations(df, df_annon, data_concat_all)
            except:
                pass

        # x_list = x_list + [df['UTM N/S(m)'].max(), df['UTM N/S(m)'].min()]
        # y_list = y_list + [df['UTM E/W(m)'].max(), df['UTM E/W(m)'].min()]
        x_list = x_list + [df['lat'].max(), df['lat'].min()]
        y_list = y_list + [df['lon'].max(), df['lon'].min()]
        z_list = z_list + [df['TVD(m RKB)'].max(), df['TVD(m RKB)'].min()]

        trace0 = go.Scatter3d(
            # x=df['UTM N/S(m)'],
            # y=df['UTM E/W(m)'],
            x=df['lat'],
            y=df['lon'],
            z=df['TVD(m RKB)'],
            mode='lines',
            line=dict(
                # color='rgb(211,211,211)',
                width=7
            ),
            hoverinfo='z',  # 'none',
            showlegend=True,
            name=well_name
        )


        annotations.append(dict(
            showarrow=False,
            # x=df['UTM N/S(m)'].iloc[-1],
            # y=df['UTM E/W(m)'].iloc[-1],
            x=df['lat'].iloc[-1],
            y=df['lon'].iloc[-1],
            z=df['TVD(m RKB)'].iloc[-1],
            text=well_name,
            xanchor="left",
            xshift=5,
            opacity=1))



        if show_dogleg:
            trace10 = go.Scatter3d(
            x=df[df['DLS(deg/30m)']<2]['lat'],
            y=df[df['DLS(deg/30m)']<2]['lon'],
            z=df[df['DLS(deg/30m)']<2]['TVD(m RKB)'],
            mode='markers',
            marker=dict(
                color='rgb(128,196,196)',
                size=5
            ),
            name='DLS (°/30m): < 2',
            text = [
                    "<b>TVD:</b> {} m<br>"
                    "<b>MD:</b> {} m<br>"
                    "<b>Inclination:</b> {} °<br>"
                    "<b>Azimuth:</b> {} °<br>"
                    "<b>DLS:</b> {} °/30m"
                    .format(
                            df['TVD(m RKB)'].loc[i],
                            df['MD(m RKB)'].loc[i],
                            df['Inc(deg)'].loc[i],
                            df['Azim(deg)'].loc[i],
                            df['DLS(deg/30m)'].loc[i]
                            )
                    for i in df[df['DLS(deg/30m)']<2].index],
            hoverinfo='text'
            )

            trace11 = go.Scatter3d(
            x=df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)]['lat'],
            y=df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)]['lon'],
            z=df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)]['TVD(m RKB)'],
            mode='markers',
            marker=dict(
                color='rgb(0,115,172)',
                size=5
            ),
            name='DLS (°/30m): 2-4',
            text = [
                    "<b>TVD:</b> {} m<br>"
                    "<b>MD:</b> {} m<br>"
                    "<b>Inclination:</b> {} °<br>"
                    "<b>Azimuth:</b> {} °<br>"
                    "<b>DLS:</b> {} °/30m"
                    .format(
                            df['TVD(m RKB)'].loc[i],
                            df['MD(m RKB)'].loc[i],
                            df['Inc(deg)'].loc[i],
                            df['Azim(deg)'].loc[i],
                            df['DLS(deg/30m)'].loc[i]
                            )
                    for i in df[(df['DLS(deg/30m)']>=2)&(df['DLS(deg/30m)']<4)].index],
            hoverinfo='text'
            )

            trace12 = go.Scatter3d(
            x=df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)]['lat'],
            y=df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)]['lon'],
            z=df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)]['TVD(m RKB)'],
            mode='markers',
            marker=dict(
                color='rgb(120,123,194)',
                size=5
            ),
            name='DLS (°/30m): 4-6',
            text = [
                    "<b>TVD:</b> {} m<br>"
                    "<b>MD:</b> {} m<br>"
                    "<b>Inclination:</b> {} °<br>"
                    "<b>Azimuth:</b> {} °<br>"
                    "<b>DLS:</b> {} °/30m"
                    .format(
                            df['TVD(m RKB)'].loc[i],
                            df['MD(m RKB)'].loc[i],
                            df['Inc(deg)'].loc[i],
                            df['Azim(deg)'].loc[i],
                            df['DLS(deg/30m)'].loc[i]
                            )
                    for i in df[(df['DLS(deg/30m)']>=4)&(df['DLS(deg/30m)']<6)].index],
            hoverinfo='text'
            )

            trace13 = go.Scatter3d(
            x=df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)]['lat'],
            y=df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)]['lon'],
            z=df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)]['TVD(m RKB)'],
            mode='markers',
            marker=dict(
                color='rgb(183,18,124)',
                size=5
            ),
            name='DLS (°/30m): 6-8',
            text = [
                    "<b>TVD:</b> {} m<br>"
                    "<b>MD:</b> {} m<br>"
                    "<b>Inclination:</b> {} °<br>"
                    "<b>Azimuth:</b> {} °<br>"
                    "<b>DLS:</b> {} °/30m"
                    .format(
                            df['TVD(m RKB)'].loc[i],
                            df['MD(m RKB)'].loc[i],
                            df['Inc(deg)'].loc[i],
                            df['Azim(deg)'].loc[i],
                            df['DLS(deg/30m)'].loc[i]
                            )
                    for i in df[(df['DLS(deg/30m)']>=6)&(df['DLS(deg/30m)']<8)].index],
            hoverinfo='text'
            )

            trace14 = go.Scatter3d(
            x=df[df['DLS(deg/30m)']>8]['lat'],
            y=df[df['DLS(deg/30m)']>8]['lon'],
            z=df[df['DLS(deg/30m)']>8]['TVD(m RKB)'],
            mode='markers',
            marker=dict(
                color='rgb(204,19,51)',
                size=5
            ),
            name='DLS (°/30m): > 8',
            text = [
                    "<b>TVD:</b> {} m<br>"
                    "<b>MD:</b> {} m<br>"
                    "<b>Inclination:</b> {} °<br>"
                    "<b>Azimuth:</b> {} °<br>"
                    "<b>DLS:</b> {} °/30m"
                    .format(
                            df['TVD(m RKB)'].loc[i],
                            df['MD(m RKB)'].loc[i],
                            df['Inc(deg)'].loc[i],
                            df['Azim(deg)'].loc[i],
                            df['DLS(deg/30m)'].loc[i]
                            )
                    for i in df[df['DLS(deg/30m)']>8].index],
            hoverinfo='text'
            )
        
            data = data + [trace10, trace11, trace12, trace13, trace14]

        data = data + [trace0]

    #concat an empty operation csv just in case all chosen wells does not contain an operation csv
    data_concat_all = pd.concat([data_concat_all ,pd.read_csv('operation_csv/blank_operation.csv', sep=';')],
                                ignore_index = True,
                                sort = False).sort_values('MD(m RKB)')

    if show_incidents:
        try:
            trace1 = go.Scatter3d(
                # x=data_concat_all[data_concat_all['Report'] == 'Stuck pipe']['UTM N/S(m)'],
                # y=data_concat_all[data_concat_all['Report'] == 'Stuck pipe']['UTM E/W(m)'],
                x=data_concat_all[data_concat_all['Report'] == 'Stuck pipe']['lat'],
                y=data_concat_all[data_concat_all['Report'] == 'Stuck pipe']['lon'],
                z=data_concat_all[data_concat_all['Report'] == 'Stuck pipe']['TVD(m RKB)'],
                mode='markers',
                marker=dict(
                    color='rgb(100,100,180)',
                    size=8
                ),
                name='Stuck pipe'  # ,
            
            )
            trace2 = go.Scatter3d(
                # x=data_concat_all[data_concat_all['Report'] == 'Loss']['UTM N/S(m)'],
                # y=data_concat_all[data_concat_all['Report'] == 'Loss']['UTM E/W(m)'],
                x=data_concat_all[data_concat_all['Report'] == 'Loss']['lat'],
                y=data_concat_all[data_concat_all['Report'] == 'Loss']['lon'],
                z=data_concat_all[data_concat_all['Report'] == 'Loss']['TVD(m RKB)'],
                mode='markers',
                marker=dict(
                    color='rgb(128,196,196)',
                    size=8
                ),
                name='Loss'  
                
            )

            data = data + [trace1, trace2]
        except:
            pass


    





    #data = data #+ [trace1, trace2]
    x = max(x_list) - min(x_list)
    y = max(y_list) - min(y_list)
    z = max(z_list) - min(z_list)

    layout = dict(
        #width=1100,
        #height=1200,
        margin={"r":0,"t":0,"l":0,"b":100},
        autosize=True,
        legend=dict(x=0.85, y=0.85),
        hoverlabel=dict(
            bgcolor='rgb(255,255,255)',
            bordercolor='rgb(0,0,0)'
        ),
        hovermode='closest',
        scene=dict(
            xaxis=dict(
                title='<b>Latitude</b>',
                gridcolor='rgb(169,169,169)',
                zerolinecolor='rgb(169,169,169)',
                showbackground=True,
                backgroundcolor='rgb(255,255,255)',
                showspikes=False,
                tickformat =".3f",
                tickmode = 'array'
            ),
            yaxis=dict(
                title='<b>Longitude</b>',
                gridcolor='rgb(169,169,169)',
                zerolinecolor='rgb(169,169,169)',
                showbackground=True,
                backgroundcolor='rgb(255,255,255)',
                showspikes=False,
                tickformat =".3f" ,
                tickmode = 'array'
            ),
            zaxis=dict(
                title='<b>TVD(m RKB)</b>',
                gridcolor='rgb(169,169,169)',
                zerolinecolor='rgb(169,169,169)',
                showbackground=True,
                backgroundcolor='rgb(255,255,255)',
                showspikes=False,
                autorange='reversed'
            ),
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=2#1
                ),
                eye=dict(
                    x=1.7,#-1.25,
                    y=1.7,#1.25,
                    z=0.1#0.5,
                )
            ),
            #aspectratio=dict(x=x / z, y=y / z, z=1),
          #  aspectmode='manual',
            annotations=annotations
        )
    )


    fig22 = go.Figure(data=data, layout=layout)
    #fig22.show()

    return fig22