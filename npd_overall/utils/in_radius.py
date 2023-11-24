from math import radians, cos, sin, asin, sqrt
import pandas as pd
well_data_orig = pd.read_csv('npd_overall/Explo_and_Dev_concat_wells.csv')   


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles

    return c * r
def if_in_distance(radius, lon1,lat1):
    """_summary_

    :param float radius: kilometers
    :param _type_ lon1: _description_
    :param _type_ lat1: _description_
    :return _type_: _description_
    """
    in_distance_list=[]
    for i in range(len(well_data_orig)):
        for  lon2, lat2 in [well_data_orig.iloc[i][["wlbEwDesDeg","wlbNsDecDeg"]].values]:
            aa = haversine(lon1, lat1, lon2, lat2)
            if aa <= radius:
                in_distance_list.append(well_data_orig.iloc[i]['wlbWellboreName'])
            else:
                pass

    return in_distance_list
