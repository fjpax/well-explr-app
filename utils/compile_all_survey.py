import pandas as pd
import os
import utm

def convert_utm_to_lat_lon(src_file_path):
    df = pd.read_csv(src_file_path,sep=',')
    df.rename(columns = {'UTM_N_S':'UTM N/S(m)', 'UTM_E_W':'UTM E/W(m)'}, inplace = True)
    #change column of utm from adrian's work
    try:
        df.rename(columns = {'UTM_N_S':'UTM N/S(m)', 'UTM_E_W':'UTM E/W(m)'}, inplace = True)
        df.rename(columns = {'TVD':'TVD(m RKB)', 'DEPTH':'MD(m RKB)'}, inplace = True)
        print('1')
        
    except:
        print('2')
        pass

    #convert lat long

    #careful; 31 is not for all. create a dic
    #print(df.columns)
    fn = lambda row: utm.to_latlon(row['UTM E/W(m)'], row['UTM N/S(m)'], 31, northern=True)
    df[["lat","lon"]] = df.apply(fn, axis=1, result_type="expand")

    return df


def compile_suvey_data(dir_sources, compiled_dir):
    for dir_source in dir_sources:
        for well_name in os.listdir(dir_source):
            src_file_path = os.path.join(dir_source, well_name)
            comp_file_path = os.path.join(compiled_dir, well_name)
            # checking if it is a file
            print(well_name)
            if well_name =='.DS_Store':
                continue
            if os.path.isfile(src_file_path):
                new_df = convert_utm_to_lat_lon(src_file_path)
                new_df.to_csv(comp_file_path, sep=',')
if __name__ == "__main__":
    compile_suvey_data(['/Users/2924441/Desktop/phd part 2/add_fm_data/aker_bp_data/survey',
                        '/Users/2924441/Desktop/phd part 2/add_fm_data/volve/survey_csv'], 

                        '/Users/2924441/Desktop/phd part 2/add_fm_data/all_survey_csv')