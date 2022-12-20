from dash import html
import dash_bootstrap_components as dbc
import dash


dash.register_page(__name__)

# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Page 33")),
        html.Br(),
        html.Hr(),
        dbc.Col([
            html.P("This is column 33."), 
            dbc.Button("Test Button", color="primary")
        ]), 
        dbc.Col([
            html.P("This is column 2."), 
            html.P("You can add many cool components using the bootstrap dash components library."),
        ])
    ])
    ],fluid=True)

# layout = html.Div([nav,
#     html.H1(children='This is our Archive page'),

#     html.Div(children='''
#         This is our Archive page content.
#     ''')])