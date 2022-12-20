

import pandas as pd
import plotly.express as px
import geojson
import pickle
###########
def pickle_active_lic_plotly_figure():
    f = open('npd_overall/NEWactive_license.json' ,'r+', encoding="utf-8")
    gj = geojson.load(f)
            #geodatadf
    df = pd.read_csv('npd_overall/processedActiveGeoDF.csv')
            
            #layer for licences

    figdf = px.choropleth_mapbox(df, geojson=gj, locations='prlName', hover_name="cmpLongName",
                                #color="cmpLongName",
                                #  color_continuous_scale="Viridis",
                                #range_color=(0, 12),
                                mapbox_style="carto-positron",
                                #zoom=2, center = {"lat": well_data["wlbNsDecDeg"].mean()+5, "lon": well_data["wlbEwDesDeg"].mean()+5},
                                #zoom=2, center = {"lat": 65.7, "lon": 9},
                                featureidkey="properties.prlName",
                                opacity=0.3,
                                labels={'unemp':"cmpLongName"}
                                )


    filename = 'npd_overall/active_licenses_figure.pkl'
    outfile = open(filename,'wb')
    pickle.dump(figdf,outfile)
    outfile.close()

if __name__ == '__main__':
    pickle_active_lic_plotly_figure()