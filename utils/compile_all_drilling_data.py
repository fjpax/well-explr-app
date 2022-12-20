import shutil
import os
import pandas as pd
import numpy as np
import sys
sys.path.insert(1, '/Users/2924441/Desktop/phd part 2/add_fm_data')

def get_the_bit_size_from_name(x):
    position_ =  x.rfind('_')
    bit_size = x[position_+1:]


    return bit_size

def filter_fm_is_in_drilling_data(x):
    position_ = x.rfind('_time_')
    name = x[:position_]
    return name




def compile_all_drilling_data(dir_drilling_data, destination_drilling_data):
    list_of_drilling_data = os.listdir(dir_drilling_data)
    list_of_drilling_data = list(map(lambda x: x.replace('in.csv', '') ,list_of_drilling_data))
    try:
        list_of_drilling_data.remove('.DS_Store')
    except:
        pass
    print('list_of_drilling_data:',list_of_drilling_data)
    #remove_time and .csv in names
    unique_file_names  = list(set(list(map(lambda x: filter_fm_is_in_drilling_data(x), list_of_drilling_data))))
    print('unique_file_names:',unique_file_names)
  
    for well_name in unique_file_names:
        current_drilling_data_without_fm = list(filter(lambda x:well_name == filter_fm_is_in_drilling_data(x), list_of_drilling_data))
        print('well_name:',well_name)
        print('current_drilling_data_without_fm:',current_drilling_data_without_fm)

        if current_drilling_data_without_fm:
            list_of_hole_sizes_per_well =  list(map(lambda x: get_the_bit_size_from_name(x),current_drilling_data_without_fm))
      
            drilling_data_concat = pd.DataFrame()
         
            for well_size in list_of_hole_sizes_per_well: 
                ddata = pd.read_csv(dir_drilling_data+'/' + well_name+ '_time_' + str(well_size) +'in.csv', sep=',')
                ddata.drop(ddata.columns[ddata.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
                ddata['bit_size (in)'] = well_size
                drilling_data_concat = pd.concat([drilling_data_concat, ddata],
                                ignore_index = True,
                                sort = False).sort_values('HoleDepth(m)')
            drilling_data_concat.to_csv( destination_drilling_data+'/'+well_name+'.csv', sep=',')
            print('new csv saved')
            print(drilling_data_concat.shape)   


if __name__ == "__main__":
        compile_all_drilling_data(dir_drilling_data='/Users/2924441/Desktop/phd part 2/add_fm_data/aker_bp_data/drilling_data', destination_drilling_data='/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_data')
        compile_all_drilling_data(dir_drilling_data='/Users/2924441/Desktop/phd part 2/add_fm_data/volve/drilling_data', destination_drilling_data='/Users/2924441/Desktop/phd part 2/add_fm_data/all_drill_data')         
