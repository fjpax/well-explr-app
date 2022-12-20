
import dash

from dash import Input, Output, State, html, Dash

import dash_bootstrap_components as dbc

app = Dash(__name__)
server = app.server
app.config['suppress_callback_exceptions']=True




# app = dash.Dash(__name__, 
#                 external_stylesheets=[dbc.themes.BOOTSTRAP], 
#                 meta_tags=[{"name": "viewport", "content": "width=device-width"}],
#                 suppress_callback_exceptions=True)




from dash import Dash, html, dcc

#import sys
# from components import nav2, about
# # Define the navbar
# nav = nav2.layout

#sys.path.insert(1, '/Users/2924441/Desktop/phd part 2/add_fm_data')





################
# from pages.nav2 import my_nav_bar

# app = Dash(__name__, use_pages=True,
#             external_stylesheets=[dbc.themes.BOOTSTRAP], 
#             meta_tags=[{"name": "viewport", "content": "width=device-width"}],
#             suppress_callback_exceptions=True)
# # Define the index page layout
# app.layout = html.Div([
#    # dcc.Location(id='url', refresh=False),
#     my_nav_bar(), 
#     dbc.Container([dash.page_container], 
#     fluid=True), 
# ])

################
# if __name__ == '__main__':
# 	app.run_server(debug=False, port=8059)       
    
