import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import json
# formation_lists =['Asgard','Base Utsira',
#                      'Tor','Skade','Grid','Base Grid',
#                      'Blodoeks','Ty','Heather','Hugin',
#                      'Ekofisk','Utsira','Undifferentiated','Grid base',
#                      'Blodoks','Sele','Rodeby','TD','Balder',
#                      'Heather SST','Sleipner','Base Skade','Hod',
#                      'Draupne','Hidra','Hugin base','Rodby','Lista','Roedby','Asgard',
#                      'Undifferentiated Hordaland','Top Grid','Undifferentiated Nordaland',
#                      'Top Balder','Top Heimdal']
# formation_lists.remove('TD')

# #list of colors
# color_lists = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
#                 'beige', 'bisque', 'dimgrey', 'blanchedalmond', 'deepskyblue',
#                 'blueviolet', 'brown', 'burlywood', 'cadetblue',
#                 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
#                 'cornsilk', 'crimson', 'cyan', 'darkcyan',
#                 'darkgoldenrod', 'darkgray', 'darkgreen',
#                 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
#                 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
#                 'darkslateblue', 'darkslategray', 'darkslategrey',
#                 'darkturquoise', 'darkviolet', 'deeppink', 
#                 'dimgray',  'dodgerblue', 'firebrick'
#                 ]
# fm_color_dict = dict(zip(formation_lists, color_lists[:len(formation_lists)]))
# fm_color_dict
f = open('/Users/2924441/Desktop/phd part 2/add_fm_data/fm_color_dict.json')
fm_color_dict = json.load(f)
 

def viz_formation_as_add_hrect(well_name, fig, column_num):
    """visualize the formation by depth

    :param _type_ well_names: _description_
    """
    my_well = pd.read_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/all_fm/'+well_name+'.csv', sep=';')

    #zip formation, and depth range
    my_well= my_well[my_well['Formation Tops'].notna()]
    assert my_well['Formation Tops'][-1:].iat[-1] =='TD'
    fm_depthrange_list = zip(my_well['Formation Tops'][:-1],my_well['m MD'][:-1], my_well['m MD'][1:])


    for formation, top_depth, both_depth in fm_depthrange_list:
        fig.add_hrect(y1=both_depth, y0=top_depth, 
                            line_width=0, row=1, col=column_num, 
                            fillcolor=fm_color_dict[formation], 
                            opacity=1,annotation_text=formation, 
                            annotation_position="inside left")
 
                              
    return fig

def viz_rop_formation(well_names):
    num_wells = len(well_names)
    fig = make_subplots(rows=1, cols=num_wells*2, shared_yaxes=True, column_widths=[0.3,0.7]*num_wells,horizontal_spacing = 0)
    # max_rop =[]
    # min_rop =[]
    max_depth =[]
    min_depth =[]
    for i, well_name in enumerate(well_names,1):
        drilling_data = pd.read_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_with_fm_csv/'+well_name+'.csv',dtype={'hole_size': float,'Well_name':str}) 

        fig.add_trace(go.Scatter(x=drilling_data['Time Averaged ROP m/h'], y=drilling_data['HoleDepth(m)'], name=well_name),
                  row=1, col=i*2)

        fig.add_trace(go.Scatter(x=[], y=[]),
                  row=1, col=(i*2)-1)
            
        #fig = viz_formation_with_depth(well_name, fig,(i*2)-1)
        fig =viz_formation_as_add_hrect(well_name, fig,(i*2)-1)
            
        
            # max_rop.append(max(drilling_data['HoleDepth(m)']))
            # min_rop.append(min(drilling_data['HoleDepth(m)']))
        max_depth.append(max(drilling_data['HoleDepth(m)']))
        min_depth.append(min(drilling_data['HoleDepth(m)']))

      
    fig.update_layout(height=750, width=400*num_wells,
                        title_text="ROP and Formations", 
                        title_x=0.5,
                        autosize=True,
                        margin=dict(
                                    l=10,
                                    r=10,
                                    b=10,
                                    t=30,
                                    pad=4
                                    ),
                        xaxis2=dict(title='ROP (m/hr)'),
                        xaxis4=dict(title='ROP (m/hr)'),
                        xaxis6=dict(title='ROP (m/hr)'),
                        xaxis1=dict(title='ROP (m/hr)',visible=False, showticklabels=False),
                        xaxis3=dict(title='ROP (m/hr)',visible=False, showticklabels=False),
                        xaxis5=dict(title='ROP (m/hr)',visible=False, showticklabels=False),
                             

                        yaxis = dict(showgrid = True, range=[max(max_depth),min(min_depth)],
                                    tickmode = 'linear', title='Measured Depth (m)',
                                    dtick = 100) )
                        
    #fig.show()

    return fig





