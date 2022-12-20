from dash import html, dcc, Dash
from dash.dependencies import Input, Output, State
import sys
import dash_bootstrap_components as dbc
from pages import about
sys.path.insert(1, '/Users/2924441/Desktop/phd part 2/add_fm_data')
# Connect to main app.py file
from old_pages.app import app

from pages.Drilling_page import casings,drilling
#



# Connect the navbar to the index
from . import nav

# Define the navbar
nav = nav.layout

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    dbc.Container([html.Div(id='page-content', children=[])], fluid=True), 
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/drillings':
        return drilling.layout
    if pathname == '/casings':
        return casings.layout
    if pathname == '/about':
        return about.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=False,port=8053)