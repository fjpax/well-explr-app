from matplotlib.pyplot import legend
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

color_seq= px.colors.qualitative.Plotly


def viz_averop_formation(well_names:list,formation='all'):
    """visualize average ROP and include depth drilled per formation shown as bar chart

    :param list well_names: _description_
    :param str formation: _description_, defaults to 'all'
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if formation =='all':
        for i,well in enumerate(well_names):

            drilling_data = pd.read_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_with_fm_csv/'+well+'.csv',sep=',',dtype={'hole_size': float,'Well_name':str}) 
       
            drilling_data = drilling_data.groupby(['Well_name', 'formation'], as_index = False).agg(
                {'HoleDepth(m)': ['mean', 'min', 'max'],'Time Averaged ROP m/h':['mean']})
            drilling_data['MD_per_drilled_fm'] =drilling_data['HoleDepth(m)']['max'] - drilling_data['HoleDepth(m)']['min']
            drilling_data

            fig.add_trace(go.Scatter(
                            x=drilling_data['formation'], y=drilling_data['Time Averaged ROP m/h']['mean'],
                            mode='markers',
                            name=drilling_data['Well_name'][0]+ ' ROP',
                            marker=dict(
                                    color=color_seq[i],size=12
                            )),
                            secondary_y=False
                        )

            fig.add_trace(go.Bar(
                            x= drilling_data['formation'], 
                            y=drilling_data['MD_per_drilled_fm'], 
                            name=drilling_data['Well_name'][0] + ' Depth Drilled',
                            marker_color=color_seq[i],
                            opacity=0.3,
                            width=0.4),
                         secondary_y=True
                     )
    fig.update_layout(barmode='overlay',margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_yaxes(title_text="<b>Ave ROP (m/hr)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Depth Drilled per formation (m)</b>", secondary_y=True)
    fig['layout']['yaxis2']['showgrid'] = False
    #fig.show()
    return fig
#viz_averop_formation(['F-11A','F-15A','F-1C'])        