import pandas as pd
import numpy as np
import sys
# sys.path.insert(1, '/Users/2924441/Desktop/phd part 2/add_fm_data')
sys.path.insert(1)

import os

def get_the_bit_size_from_name(x):
    position_ =  x.rfind('_')
    bit_size = x[position_+1:]


    return bit_size

def filter_fm_is_in_drilling_data(x):
    position_ = x.rfind('_time_')
    name = x[:position_]
    return name

def add_formation_data(dir_drilling_data, dir_fm_data, dir_final_ddata_with_fm):
    list_of_drilling_data_with_fm = os.listdir('all_drill_with_fm_csv')
    try:
        list_of_drilling_data_with_fm.remove('.DS_Store')
    except:
        pass
  
    list_of_fm = os.listdir(dir_fm_data)

    try:
        list_of_fm.remove('.DS_Store')
    except:
        pass

    list_of_drilling_data_without_fm =  os.listdir(dir_drilling_data)
    try:
        list_of_drilling_data_without_fm.remove('.DS_Store')
    except:
        pass

    list_of_fms_not_included_with_drilling_data = set(list_of_fm) - set(list_of_drilling_data_with_fm)

    list_of_fms_not_included_with_drilling_data = list(map(lambda x: x.replace('.csv', '') ,list_of_fms_not_included_with_drilling_data))

    
    
    list_of_drilling_data_without_fm = list(map(lambda x: x.replace('in.csv', '') ,list_of_drilling_data_without_fm))
 
    print(list_of_fms_not_included_with_drilling_data)
    for fm_data_name in list_of_fms_not_included_with_drilling_data:
        #take the list of all drilling data with differenthole sizes
        current_drilling_data_without_fm = list(filter(lambda x:fm_data_name == filter_fm_is_in_drilling_data(x), list_of_drilling_data_without_fm))
        print('hello')
        print(current_drilling_data_without_fm)
        if current_drilling_data_without_fm:
            #take the list of all hole sizes from single well
            list_of_hole_sizes_per_well =  list(map(lambda x: get_the_bit_size_from_name(x),current_drilling_data_without_fm))
            print('list_of_hole_sizes_per_well:', list_of_hole_sizes_per_well)
            drilling_data_concat = pd.DataFrame()
            print('hello')
            for well_size in list_of_hole_sizes_per_well: 
                ddata = pd.read_csv(dir_drilling_data+'/' + fm_data_name+ '_time_' + str(well_size) +'in.csv', sep=',')
                ddata.drop(ddata.columns[ddata.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
                ddata['bit_size (in)'] = well_size
                drilling_data_concat = pd.concat([drilling_data_concat, ddata],
                                ignore_index = True,
                                sort = False).sort_values('HoleDepth(m)')
            
            fm_data = pd.read_csv(dir_fm_data+'/' + fm_data_name+'.csv', sep=';')
            fm_data.drop(fm_data.columns[fm_data.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

            fm_measured_depth = fm_data['m MD']
            fm = fm_data['Formation Tops']
            drilling_data_concat["formation"] = None
            fm_and_depth = list(zip(fm_measured_depth[:-1], fm_measured_depth[1:], fm[:-1]))
            print('hello')
            for i in fm_and_depth:
                drilling_data_concat.loc[(drilling_data_concat['HoleDepth(m)'] >= i[0]) & (drilling_data_concat['HoleDepth(m)'] <= i[1]), 'formation'] = i[2]

            drilling_data_concat['Well_name']=fm_data_name
            drilling_data_concat.to_csv(dir_final_ddata_with_fm+'/'+fm_data_name+'.csv', sep=',')
            print('new csv saved')
            print(drilling_data_concat.shape)   
                #print(drilling_data_concat)
        
  




if __name__ == "__main__":
       

        add_formation_data(dir_drilling_data='volve/drilling_data', 
                            dir_fm_data='volve/formation_data', 
                            dir_final_ddata_with_fm='all_drill_with_fm_csv')


