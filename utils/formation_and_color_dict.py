import pandas as pd
import os
import json

#list of colors
color_lists = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
                'beige', 'bisque', 'dimgrey', 'blanchedalmond', 'deepskyblue',
                'blueviolet', 'brown', 'burlywood', 'cadetblue',
                'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
                'cornsilk', 'crimson', 'cyan', 'darkcyan',
                'darkgoldenrod', 'darkgray', 'darkgreen',
                'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
                'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
                'darkslateblue', 'darkslategray', 'darkslategrey',
                'darkturquoise', 'darkviolet', 'deeppink', 
                'dimgray',  'dodgerblue', 'firebrick'
                ]
print(len(color_lists))

def get_formation_list(directory_all_fm):
    well_names = os.listdir(directory_all_fm)
    formation_lists = []
    for well_name in well_names:
        well = pd.read_csv(os.path.join(directory_all_fm,well_name), sep=';')
        well= well[well['Formation Tops'].notna()]
        well.to_csv(os.path.join(directory_all_fm,well_name), sep=';')
        print('saved new: ', well_name )



def get_color_formation_dict(directory_all_fm):
    well_names = os.listdir(directory_all_fm)
    formation_lists = []
    for well_name in well_names:
        well = pd.read_csv(os.path.join(directory_all_fm,well_name), sep=';')
        formation_lists = formation_lists+list(well['Formation Tops'])
    
 
    formation_lists = list(set(formation_lists))
    formation_lists.remove('TD')
   
    print(len(formation_lists))
 


    fm_color_dict = dict(zip(formation_lists, color_lists[:len(formation_lists)]))
    with open("fm_color_dict.json", "w") as outfile:
        json.dump(fm_color_dict, outfile)
    
if __name__ == '__main__':
    directory_all_fm = '/Users/2924441/Desktop/phd part 2/add_fm_data/all_fm'
	    
    get_formation_list(directory_all_fm)
    get_color_formation_dict(directory_all_fm)
    