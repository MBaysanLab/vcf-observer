from dash import dcc, html, get_asset_url
import dash_bootstrap_components as dbc

from layout.navbar.welcome import welcome_tab
from layout.navbar.upload import upload_tab
from layout.navbar.analyze.analyze import analyze_tab

import dash_app
from layout import ids, styles

navbar = (
    dbc.Col(
        width=3,
        style={
            'background': styles.light_gray,
            'height': '100vh',
            'paddingLeft': '1em',
            'paddingRight': '1em',
            'overflowY': 'auto',
            'overflowX': 'hidden',
            'scrollbarWidth': 'thin',
        },
        children=[
            dcc.Store(ids.navbar_navbar__first_visit_for_tabs__store, storage_type='local'),  # Persistent throughout sessions
            dcc.Store(ids.navbar_navbar__first_visit_for_buttons__store, storage_type='local'),

            html.H2(
                style={
                    'textAlign': 'center',
                    'paddingTop': '0.8em',
                    'paddingBottom': '0.5em',
                    'marginBottom': '0px',
                },
                children=[
                    html.Img(src=get_asset_url('logo.png'), style={
                        'height': '36px',
                        'width': '36px',
                        'marginRight': '0.4em',
                        'marginBottom': '12px'
                    }),
                    'VCF Observer',
                ]),

            dcc.Tabs(id=ids.navbar_navbar__tabs__tabs, value='tab-upload', style={'paddingBottom': '1.5em'}, children=[
                welcome_tab,
                upload_tab,
                analyze_tab,
            ]),
            dcc.Store(ids.navbar_navbar__session_id__store),
        ]
    )
)
