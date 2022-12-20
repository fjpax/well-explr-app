import os
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as et



import plotly.express as px
import pandas as pd
def daily_report_sun(well_name):
    df= pd.read_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/volve/daily_report/'+well_name+'.csv')
    fig = px.sunburst(df, path=['State', 'Operation'], values='Duraton_hours')
    fig.update_layout(margin={"r":0.1,"t":0.1,"l":0.1,"b":0.1})
    fig.update_traces(textinfo="label+percent parent + value")

    return fig



def get_operations(well):

    """xml to csv

    :return _type_: csv
    """

    report_list = os.listdir('/Users/2924441/Desktop/equinor volve azure/Well_technical_data/Daily Drilling Report - XML Version')

    start = []
    end = []
    md = []
    operation = []
    comment = []
    duration = []
    state = []

    df = pd.DataFrame(
        list(zip(
            start,
            end,
            md,
            duration,
            operation,
            comment,
            state
        )),
        columns = [
            'Start',
            'End',
            'MD (m)',
            'Duration',
            'Operation',
            'Comment',
            'State'
    ])

    # os.chdir('')

    for file in report_list:
        if file[:-15] == well:
            report_tree = et.parse('/Users/2924441/Desktop/equinor volve azure/Well_technical_data/Daily Drilling Report - XML Version/'+file)
            report_root = report_tree.getroot()

            start = []
            end = []
            md = []
            operation = []
            comment = []
            duration = []
            state = []

            for child in report_root:
                for elem in child:
                    if elem.tag == '{http://www.witsml.org/schemas/1series}activity':
                        for subelem in elem:
                            if 'dTimStart' in subelem.tag:
                                start.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                start_temp = datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M')
                            elif 'dTimEnd' in subelem.tag:
                                end.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                end_temp = datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M')
                            elif 'md' in subelem.tag:
                                md.append(subelem.text)
                            elif 'proprietaryCode' in subelem.tag:
                                operation.append(subelem.text)
                            elif 'comments' in subelem.tag:
                                comment.append(subelem.text)
                            elif 'stateDetailActivity' in subelem.tag:
                                state.append(subelem.text)
                            else:
                                pass
                            
                        duration.append((end_temp-start_temp))


            df = df.append(
                pd.DataFrame(
                    list(zip(
                        start,
                        end,
                        md,
                        duration,
                        operation,
                        comment,
                        state
                    )),
                    columns = [
                        'Start',
                        'End',
                        'MD (m)',
                        'Duration',
                        'Operation',
                        'Comment',
                        'State'
                    ]),
                ignore_index = True,
                sort = False
            )

    df.sort_values(['Start'], inplace=True)
    def convert_duration_hour(x):
        return round(x.total_seconds()/ 3600,2)

    df['Duraton_hours'] = df['Duration'].map(convert_duration_hour)

    os.chdir('../')
    df.to_csv('/Users/2924441/Desktop/phd part 2/add_fm_data/volve/daily_report/'+well+'.csv')
    return df


if __name__ == '__main__':
    get_operations('15_9_F_15')
    get_operations('15_9_F_1_C')
    get_operations('15_9_F_11_A')
