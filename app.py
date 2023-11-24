import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key=os.environ.get('OPENAI_API_KEY')

import dash


from dash import Output, State, html, Dash, dcc,Input
#from dash import html, Dash
import dash_bootstrap_components as dbc



# Define the navbar
from components.nav import my_nav_bar


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    my_nav_bar(), 
    dbc.Container([html.Div(dash.page_container)], fluid=True)
    
    
    

],style={"height": "100%"})


if __name__ == '__main__':
	app.run_server(debug=True,port=8066)

