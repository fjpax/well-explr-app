import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash, dcc
from dash_bootstrap_components._components.Container import Container


import base64






print('page_registry: ',dash.page_registry, '//////')

def my_nav_bar():
    PLOTLY_LOGO = "digiwells.png"
    print('page_registry: ',dash.page_registry['pages.stratigraphy_pages.formations']['path'], '//////')
    print('page_registry: ',dash.page_registry['pages.Users.2924441.Desktop.phd part 2.add_fm_data.pages.well_summary_pages.well_comparer']['path'], '//////')
    search_bar = dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Search")),
            dbc.Col(
                dbc.Button(
                    "Search", color="primary", className="ms-2", n_clicks=1
                ),
                width="auto",
            ),
        ],
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )

    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
              
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('assets/digiwells.png', 'rb').read()).decode('ascii')), height="30px")),
                            dbc.Col(dbc.NavbarBrand("Explr", className="ms-2",href='/overview')),
                            dbc.Col(dbc.DropdownMenu(
                                        [dbc.DropdownMenuItem("Overview",href='/overview')],# '/analytics'
                                        
                                        label="Overview",
                                        nav=True, className="ms-2",
                                    )),
                            dbc.Col(dbc.DropdownMenu(
                                        [dbc.DropdownMenuItem("Survey",href='/drilling'), 
                                        dbc.DropdownMenuItem("Casings",href='/casings'),
                                        dbc.DropdownMenuItem("Formations",href='/formation'),
                                        dbc.DropdownMenuItem("Well Compare",href='/well-comparer')],
                                        label="Drilling",
                                        nav=True, className="ms-2",
                                    )),
                            dbc.Col(dbc.DropdownMenu(
                                        [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
                                        label="Completion",
                                        nav=True, className="ms-2",
                                    )),
                            dbc.Col(dbc.DropdownMenu(
                                        [dbc.DropdownMenuItem("Item 1"), dbc.DropdownMenuItem("Item 2")],
                                        label="Production",
                                        nav=True, className="ms-2",
                                    )),
                                    #,href=dash.page_registry['pages.Stratigraphy_page.formations']['path']
                            dbc.Col(dbc.DropdownMenu(
                                        [dbc.DropdownMenuItem("Formations and ROP", href ='/formations'), 
                                        dbc.DropdownMenuItem("Item 2")],
                                        label="Stratigraphy",
                                        nav=True, className="ms-2",
                                    )),
                            dbc.Col(dbc.DropdownMenu(
                                        [dcc.Link("Bot",href ='https://dd3mo8e3y98w3.cloudfront.net/index.html')],
                                        label="Help",
                                        nav=True, className="ms-2",
                                    )),
                        ],
                        align="center",
                        className="g-0",
                    ),
                           


                    href='/overview',#about
                    style={"textDecoration": "none"},
            ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    search_bar,
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True),

          
            ] 
        ),
        color="dark",
        dark=True,
    )
    return navbar 
