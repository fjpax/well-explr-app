import os
import re
import pandas as pd
def convert_survey_txt_to_csv(filepath,well_name,csv_directory):
    """convert survey file from txt file to csv from volve

    :param _type_ filepath: _description_
    :param _type_ well_name: _description_
    :param _type_ csv_directory: _description_
    """

    f = open(filepath, 'r', encoding = "ISO-8859-1")

    content = f.readlines()
    for i in range(len(content)):
        if ''.join(content[i].split()) == 'SURVEYLIST':
            survey = i
            print(survey)
            break
    lists_list = []
    for line in content[i+1:]:
            line = line.strip()
            # string with multiple consecutive spaces
            s = line.replace('\n',"")
            # make spaces consistent
            s = re.sub("  +", "*", s)
            s = s.split('*')
            assert len(s) ==9
            lists_list.append(s)
    df = pd.DataFrame(lists_list[2:], columns =[m+'('+n+')' for m,n in zip(lists_list[0],lists_list[1])])
    df.to_csv(csv_directory+'/'+well_name+'.csv', sep=',')
    print('saved:', well_name)

if __name__ == "__main__":
    # assign directory
    directory_txt = '/Users/2924441/Desktop/equinor volve azure/survey'
    directory_csv ='volve/survey_csv'
    # iterate over files in
    # that directory
    for well_name in os.listdir(directory_txt):
        file_path = os.path.join(directory_txt, well_name)
        # checking if it is a file
        print(well_name)
        if well_name =='.DS_Store':
            continue
        if os.path.isfile(file_path):
            convert_survey_txt_to_csv(file_path,well_name,directory_csv)
