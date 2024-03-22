from dash import dcc
import dash_bootstrap_components as dbc

from layout.display import welcome, upload, analyze

display = dbc.Col(
    width=9,
    style={
        'paddingLeft': '0',
        'paddingRight': '0',
        'height': '100vh',
        'overflow': 'auto',
    },
    children=[dcc.Loading([
        welcome.welcome_display,
        upload.upload_display,
        analyze.analyze_display,
    ])]
)
