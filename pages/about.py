import dash
from dash import html, dcc


import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, callback
from dash_bootstrap_components._components.Container import Container


dash.register_page(__name__)


# Import necessary libraries 
from dash import html
import dash_bootstrap_components as dbc

items = [
    dbc.DropdownMenuItem("Item 1"),
    dbc.DropdownMenuItem("Item 2"),
    dbc.DropdownMenuItem("Item 3"),
]


dropdowns = html.Div(
    [
        dbc.DropdownMenu(
            items, label="Primary", color="primary", className="m-1"
        ),
        dbc.DropdownMenu(
            items, label="Secondary", color="secondary", className="m-1"
        ),
        dbc.DropdownMenu(
            items, label="Success", color="success", className="m-1"
        ),
        dbc.DropdownMenu(
            items, label="Warning", color="warning", className="m-1"
        ),
        dbc.DropdownMenu(
            items, label="Danger", color="danger", className="m-1"
        ),
        dbc.DropdownMenu(items, label="Info", color="info", className="m-1"),
    ],
    style={"display": "flex", "flexWrap": "wrap"},
)


layout = html.Div([
            dbc.Row([
                dbc.Button(
                    "Open collapse",
                    id="collapse-button",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    html.Div([
                    dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                    dropdowns]),
                    
                    id="collapse",
                    is_open=False,
                )])

                ])

@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open











# Define the page layout
# layout = dbc.Container([
#     dbc.Row([
#         html.Center(html.H1("Page 1")),
#         html.Br(),
#         html.Hr(),
#         dbc.Col([
#             html.P("This is column 1."), 
#             dbc.Button("Test Button", color="primary")
#         ]), 
#         dbc.Col([
#             html.P("This is column 2."), 
#             html.P("You can add many cool components using the bootstrap dash components library."),
#         ])
#     ])
# ], fluid=True)


