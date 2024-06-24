from dash import html, get_asset_url

import dash_app
from layout import ids, styles

welcome_display = (
    html.Div(id=ids.display_welcome__display__div, style=styles.display_pane, children=[
        html.Div(style={'textAlign': 'center', 'paddingTop': '2.4em', 'paddingBottom': '1.5em'}, children=[
            html.H3('A VCF analysis web app'),
            html.H6('for you to perform comparisons and analyses on VCF files directly from your browser.'),
        ]),
        html.Div(style={'display': 'flex', 'justifyContent': 'center', 'padding': '2em'}, children=[
            html.Div([
                html.Span('You can:', style={'fontWeight': 'bold'}),
                html.Ul(style={'fontSize': 'large'}, children=[
                    html.Li('Compare VCFs'),
                    html.Li('Find groups of interest'),
                    html.Li('Benchmark calls'),
                ]),
            ]),
            html.Div(style={'paddingLeft': '5%', 'paddingRight': '5%'}, children=[
                html.Span('With these visualisations:', style={'fontWeight': 'bold'}),
                html.Ul(style={'fontSize': 'large'}, children=[
                    html.Li('Venn diagrams'),
                    html.Li('Clustergrams'),
                    html.Li('Precision-recall plots'),
                ]),
            ]),
            html.Div([
                html.Span('With preprocessing such as:', style={'fontWeight': 'bold'}),
                html.Ul(style={'fontSize': 'large'}, children=[
                    html.Li('Dynamic grouping'),
                    html.Li('Genomic regions filtering'),
                    html.Li('PASS filtering'),
                ]),
            ]),
        ]),
        html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
            html.Img(src=get_asset_url('demo-images/demo-venn.png'), style=styles.demo_image),
            html.Img(src=get_asset_url('demo-images/demo-clustergram.png'), style=styles.demo_image),
            html.Img(src=get_asset_url('demo-images/demo-prerec.png'), style=styles.demo_image),
        ]),
    ])
)
