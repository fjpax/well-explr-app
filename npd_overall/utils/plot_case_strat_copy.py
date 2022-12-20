import plotly.graph_objects as go

import numpy as np

def cylinder(d, h, a =0, nt=100, nv =50):
    """
    parametrize the cylinder of dia d, height h, base point a
    """
    theta = np.linspace(0, 2*np.pi, nt)
    v = np.linspace(a, a+h, nv )
    theta, v = np.meshgrid(theta, v)
    x = (d/2)*np.cos(theta)
    y = (d/2)*np.sin(theta)
    z = v
    return x, y, z

def boundary_circle(d, h, nt=100):
    """
    r - boundary circle diameter
    h - height above xOy-plane where the circle is included
    returns the circle parameterization
    """
    theta = np.linspace(0, 2*np.pi, nt)
    x= (d/2)*np.cos(theta)
    y = (d/2)*np.sin(theta)
    z = h*np.ones(theta.shape)
    return x, y, z



def plot_casing_and_statigraphy_3D(chosen_wells_list:list, stratigraphy_all_dict, well_casing_design_all_dict):
    
    for well_name in chosen_wells_list:
        chosen_well_dict= well_casing_design_all_dict[well_name]
        traces=[]
    
        for section in chosen_well_dict.keys():
            if section == 'CONDUCTOR':
                diameter = float(chosen_well_dict['CONDUCTOR']['Casingdiam.[inch]'])
                section_start = 0
                section_end = float(chosen_well_dict['CONDUCTOR']['Casingdepth[m]'])
                colorscale = [[0, 'blue'],[1, 'blue']]
                
                x, y, z = cylinder(diameter, section_end, a=section_start)

                cyl1 = go.Surface(x=x, y=y, z=z,colorscale = colorscale, showscale=False, opacity=0.5)

                
                xb_low, yb_low, zb_low = boundary_circle(diameter, h=section_start)
                xb_up, yb_up, zb_up = boundary_circle(diameter, h=section_start+section_end)

                bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                                    y = yb_low.tolist()+[None]+yb_up.tolist(),
                                    z = zb_low.tolist()+[None]+zb_up.tolist(),
                                    mode ='lines',
                                    line = dict(color='blue', width=2),
                                    opacity =0.55, showlegend=False)
                traces.append([cyl1, bcircles1])
                
                #formation
                fm1= go.Surface(x = [0,0],y = [18,23],z = [[0, section_end],[0, section_end]], colorscale =[[0,'red'],[1,'red']], showscale=False)
                fm2= go.Surface(x = [0,0],y = [23,28],z = [[0, section_end],[0, section_end]], colorscale =[[0,'violet'],[1,'violet']], showscale=False)
                traces.append([fm1, fm2])                           
            
            
            elif section == 'SURF.COND.':
                    if chosen_well_dict['SURF.COND.']['Casingdiam.[inch]']=='18 5/8': 
                        diameter = 18.625
                    else:
                        diameter = float(chosen_well_dict['SURF.COND.']['Casingdiam.[inch]'])
                    

                    section_start = 0
                    section_end = float(chosen_well_dict['SURF.COND.']['Casingdepth[m]'])
                    colorscale = [[0, 'pink'],[1, 'pink']]
                    
                    x, y, z = cylinder(diameter, section_end, a=section_start)

                    cyl1 = go.Surface(x=x, y=y, z=z,colorscale = colorscale, showscale=False, opacity=0.5)

                    
                    xb_low, yb_low, zb_low = boundary_circle(diameter, h=section_start)
                    xb_up, yb_up, zb_up = boundary_circle(diameter, h=section_start+section_end)

                    bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                                        mode ='lines',
                                        line = dict(color='pink', width=2),
                                        opacity =0.55, showlegend=False)
                    traces.append([cyl1, bcircles1])


            elif section == 'INTERM.':

                    if chosen_well_dict['INTERM.']['Casingdiam.[inch]']=='9 5/8':
                        diameter = 9.625
                    elif chosen_well_dict['INTERM.']['Casingdiam.[inch]']=='13 3/8':
                        diameter = 13.375
                    else:
                        diameter= float(chosen_well_dict['INTERM.']['Casingdiam.[inch]'])
                    section_start = 0
                    section_end = float(chosen_well_dict['INTERM.']['Casingdepth[m]'])
                    colorscale = [[0, 'green'],[1, 'green']]
                    
                    x, y, z = cylinder(diameter, section_end, a=section_start)

                    cyl1 = go.Surface(x=x, y=y, z=z,colorscale = colorscale, showscale=False, opacity=0.5)

                    
                    xb_low, yb_low, zb_low = boundary_circle(diameter, h=section_start)
                    xb_up, yb_up, zb_up = boundary_circle(diameter, h=section_start+section_end)

                    bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                                        mode ='lines',
                                        line = dict(color='green', width=2),
                                        opacity =0.55, showlegend=False)
                    traces.append([cyl1, bcircles1])
                    
                                

            elif section == 'LINER':
                    diameter = float(chosen_well_dict['LINER']['Casingdiam.[inch]'])
                    section_start = float(chosen_well_dict['LINER']['linerStartDepth'])
                    section_end = float(chosen_well_dict['LINER']['Casingdepth[m]'])
                    colorscale = [[0, 'red'],[1, 'red']]
                    
                    x, y, z = cylinder(diameter, section_end, a=section_start)

                    cyl1 = go.Surface(x=x, y=y, z=z,colorscale = colorscale, showscale=False, opacity=0.5)

                    
                    xb_low, yb_low, zb_low = boundary_circle(diameter, h=section_start)
                    xb_up, yb_up, zb_up = boundary_circle(diameter, h=section_start+section_end)

                    bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                                        mode ='lines',
                                        line = dict(color='red', width=2),
                                        opacity =0.55, showlegend=False)
                    traces.append([cyl1, bcircles1])
                
            elif section == 'OPEN HOLE':
                    
                    if chosen_well_dict['OPEN HOLE']['Holediam.[inch]']=='8 1/2':
                        diameter = 8.5
                    elif chosen_well_dict['OPEN HOLE']['Holediam.[inch]']=='12 1/4':
                        diameter = 12.25
                    elif chosen_well_dict['OPEN HOLE']['Holediam.[inch]']=='9 5/8':
                        diameter = 9.625
                    else:
                      
                        diameter= float(chosen_well_dict['OPEN HOLE']['Holediam.[inch]'])
                
                    section_start = float(chosen_well_dict['OPEN HOLE']['openHoleStartDepth'])
                    section_end = float(chosen_well_dict['OPEN HOLE']['Holedepth[m]'])
                    colorscale = [[0, 'brown'],[1, 'brown']]
                    
                    x, y, z = cylinder(diameter, section_end, a=section_start)

                    cyl1 = go.Surface(x=x, y=y, z=z,colorscale = colorscale, showscale=False, opacity=0.5)

                    
                    xb_low, yb_low, zb_low = boundary_circle(diameter, h=section_start)
                    xb_up, yb_up, zb_up = boundary_circle(diameter, h=section_start+section_end)

                    bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                                        mode ='lines',
                                        line = dict(color='brown', width=2),
                                        opacity =0.55, showlegend=False)
                    traces.append([cyl1, bcircles1])
        ######
        #formation
        formation_annotation_list=[]
        try:
            current_well_strat_list= stratigraphy_all_dict[well_name]
            for current_stratigraphy_data in current_well_strat_list:
                if current_stratigraphy_data[3]=='FORMATION':
                    fm1= go.Surface(x = [0,0],y = [18,23],z = [[current_stratigraphy_data[0], current_stratigraphy_data[1]],[current_stratigraphy_data[0], current_stratigraphy_data[1]]], 
                                    colorscale =[[0,'red'],[1,'red']], showscale=False)
                    formation_annotation_list.append(dict(showarrow=False,x=0,y=18,z=current_stratigraphy_data[0],text=current_stratigraphy_data[2],xanchor="left"))

                else:
                    fm1= go.Surface(x = [0,0],y = [23,28],z = [[current_stratigraphy_data[0], current_stratigraphy_data[1]],[current_stratigraphy_data[0], current_stratigraphy_data[1]]],
                                    colorscale =[[0,'violet'],[1,'violet']], showscale=False)
                    formation_annotation_list.append(dict(showarrow=False,x=0,y=18,z=current_stratigraphy_data[0],text=current_stratigraphy_data[2],xanchor="left"))

            
                traces.append([fm1])   

        
        except:
            pass
                    
    
        #return [item for sublist in traces for item in sublist]
                
    
        traces_flat =[item for sublist in traces for item in sublist] 
        layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=True)
        fig =  go.Figure(data=traces_flat, layout=layout)

        fig.update_layout(scene=dict(
            xaxis=dict(type="-"),
            yaxis=dict(type="-"),
            zaxis=dict(type="-"),
            annotations=formation_annotation_list))

        fig.update_layout(scene_camera_eye_z= 0.55)
        fig.update_scenes(zaxis_autorange="reversed")
        fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj
        fig.update_layout(
            autosize=False,
            width=450,
            height=600,
            margin=dict(
                l=35,
                r=35,
                b=90,
                t=50,
                pad=4),
            paper_bgcolor="LightSteelBlue")

        fig.show()
    