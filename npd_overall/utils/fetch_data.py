import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import pickle


def fetch_exploration_wells():
    ###full explo wells in dataframe
    my_url = 'https://factpages.npd.no/en/wellbore/TableView/Exploration/All'

    #open connecttion
    uClient =uReq(my_url)

    #offloads the content into variable
    page_html = uClient.read()

    page_soup = soup(page_html, "html.parser")
    link_explo_csv = page_soup.find("div", {"class":"controls"}).find_all("a")[2]['href']

    req = requests.get(link_explo_csv)
    url_content = req.content
    csv_file = open('explorationWells.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()
    return pd.read_csv('explorationWells.csv',error_bad_lines=False)

def fetch_development_wells():
    ###full development wells in dataframe
    my_url = 'https://factpages.npd.no/en/wellbore/TableView/Development'

    #open connecttion
    uClient =uReq(my_url)

    #offloads the content into variable
    page_html = uClient.read()

    page_soup = soup(page_html, "html.parser")
    link_explo_csv = page_soup.find("div", {"class":"controls"}).find_all("a")[2]['href']

    req = requests.get(link_explo_csv)
    url_content = req.content
    csv_file = open('developmentWells.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()
    return pd.read_csv('developmentWells.csv',error_bad_lines=False)


def fetch_casing_design(number_of_well_chosen=False):

    """
    returns a dictionary of each exploration well with their casing design
    """
    #get the column names:
    my_url = 'https://factpages.npd.no/en/wellbore/PageView/Exploration/All/8228'

    #open connecttion
    uClient =uReq(my_url)

    #offloads the content into variable
    page_html = uClient.read()

    page_soup = soup(page_html, "html.parser")

    divTag=page_soup.find("table",{"class":"a2342 uk-table-striped"})
    header=divTag.find('tr')
    columnNames=[]
    for head in header.find_all('th'):
            columnNames.append("".join(head.div.div.text.split()))


    
    ###link_and_wellname_dict  of exploration wells
    my_url = 'https://factpages.npd.no/en/wellbore/PageView/Exploration/All'

    #open connecttion
    uClient =uReq(my_url)

    #offloads the content into variable
    page_html = uClient.read()

    page_soup = soup(page_html, "html.parser")
    link_and_wellname_dict  ={}

    li_list  = page_soup.find("body").find_all("ul")[5].find_all("li")
    for li in li_list:
        link_and_wellname_dict[li.text] = li.a['href']

    well_names_list = list(link_and_wellname_dict.keys())
    #just to see few examples
    if number_of_well_chosen:
        well_names_list = well_names_list[:number_of_well_chosen]

    #xploration wells dictionary and their casing design
    data_dict={}
    for well_name in well_names_list:
        print(well_name)
        my_url = link_and_wellname_dict[well_name]
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close
        page_soup = soup(page_html, "html.parser")
        
        
        
        try:
            #placed try sunce for example in 1/3-13, AttributeError: 'NoneType' object has no attribute 'find'
            #divTag = page_soup.find("table",{"class":"a2342 uk-table-striped"})
            #body=divTag.find('tbody')
            #data_dict[well_name]={}
            #for tr in body.find_all('tr'):
            #        data_dict[well_name][tr.find_all('td')[0].div.div.text.strip()]={}
            #        for i in range(1,len(columnNames)):
            #                data_dict[well_name][tr.find_all('td')[0].div.div.text.strip()][columnNames[i]]=tr.find_all('td')[i].div.div.text.strip()
        
            divTag = page_soup.find("table",{"class":"a2342 uk-table-striped"})
            body=divTag.find('tbody')
            data_dict[well_name]={}
            type_casings_names = body.find_all('tr')
            for tr_1 in range(len(type_casings_names)):
                    current_type_casing_tree = type_casings_names[tr_1]
                    current_type_casing = current_type_casing_tree.find_all('td')[0].div.div.text.strip()
                    data_dict[well_name][current_type_casing]={}
                    if current_type_casing == 'OPEN HOLE':
        
                        data_dict[well_name][current_type_casing]['openHoleStartDepth']= type_casings_names[tr_1-1].find_all('td')[-5].div.div.text.strip()
                    
                    elif current_type_casing == 'LINER':
  
                        data_dict[well_name][current_type_casing]['linerStartDepth']= type_casings_names[tr_1-1].find_all('td')[-5].div.div.text.strip()

                    for i in range(1,len(columnNames)):
                        data_dict[well_name][current_type_casing][columnNames[i]]=current_type_casing_tree.find_all('td')[i].div.div.text.strip()
        
        except:
                data_dict[well_name]={}
        
    return data_dict

def fetch_stratigraphy_wells(format='dictionary'):
    ###full explo wells in dataframe
    my_url = 'https://factpages.npd.no/en/strat/TableView/Wellbores'

    #open connecttion
    uClient =uReq(my_url)

    #offloads the content into variable
    page_html = uClient.read()

    page_soup = soup(page_html, "html.parser")
    link_stratigraphy_csv = page_soup.find("div", {"class":"controls"}).find_all("a")[2]['href']

    req = requests.get(link_stratigraphy_csv)
    url_content = req.content
    csv_file = open('stratigraphy.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()

    xxx =  pd.read_csv('stratigraphy.csv',error_bad_lines=False)

    new_xx=xxx.groupby('wlbName')[['lsuTopDepth','lsuBottomDepth','lsuName','lsuLevel']].agg(lambda x: x.tolist())

    well_stratigraphy_dict={}
    for well in new_xx.index:
        well_stratigraphy_dict[well]=list(zip(new_xx.loc[well][0],new_xx.loc[well][1],new_xx.loc[well][2],new_xx.loc[well][3]))

    a_file = open("wellStratigraphy.pkl", "wb")
    pickle.dump(well_stratigraphy_dict, a_file)
    a_file.close()

    a_file = open("wellStratigraphy.pkl", "rb")
    output = pickle.load(a_file)
    if format=='dictionary':
        return output
    else:
        return  pd.read_csv('stratigraphy.csv',error_bad_lines=False)



def fetch_field_names_and_link():
    my_url = 'https://factpages.npd.no/en/field/PageView/All'

    #open connecttion
    uClient =uReq(my_url)

    #offloads the content into variable
    page_html = uClient.read()

    page_soup = soup(page_html, "html.parser")
    field_link_and_wellname_dict  ={}

    li_list  = page_soup.find("body").find_all("ul")[7].find_all("li")
    li_list
    for li in li_list:
        field_link_and_wellname_dict [li.text] = li.a['href']

    
    return field_link_and_wellname_dict 

def fetch_explo_and_dev_wells_from_each_field(field_link_and_wellname_dict =fetch_field_names_and_link()):
    #for field_name in field_link_and_wellname_dict.keys()[0]:
    field_wells_dict={}
    for field_name in field_link_and_wellname_dict.keys():
        my_url = field_link_and_wellname_dict[field_name]
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close
        page_soup = soup(page_html, "html.parser")
        

        #exploration wells
        divTag = page_soup.find("table",{"class":"a1447 uk-table-striped"})
        body=divTag.find('tbody')
        field_wells_dict[field_name]={}
        field_wells_dict[field_name]['exploration']={}

        field_wells= body.find_all('tr')
        field_wells_list =[]
        for well in field_wells:
            field_wells_list.append(well.find_all('td')[0].div.div.text.strip())
        field_wells_dict[field_name]['exploration']=field_wells_list

        #development wells:

        divTag = page_soup.find("table",{"class":"a1523 uk-table-striped"})
        body=divTag.find('tbody')
        field_wells_dict[field_name]['development']={}

        field_wells= body.find_all('tr')
        field_wells_list =[]
        for well in field_wells:
            field_wells_list.append(well.find_all('td')[0].div.div.text.strip())
        field_wells_dict[field_name]['development']=field_wells_list
        

    return field_wells_dict


    