from dash import dcc, html

from layout import components, ids, styles

welcome_tab = dcc.Tab(label='Welcome', value='tab-welcome', style=styles.tab, selected_style=styles.tab_selected, children=[
    html.Div(style={'textAlign': 'left', 'paddingBottom': '4em', 'paddingLeft': '10%', 'paddingRight': '10%'}, children=[
        html.H6('1. Upload your VCFs', style={'paddingTop': '2.4em'}),
        html.Div('You can upload optional files such as CSVs and BEDs as well.', style={'paddingLeft': '1em', 'paddingRight': '1em'}),

        html.H6('2. Select analysis options', style={'paddingTop': '1.2em'}),
        html.Div('Analysis types and their options will be shown in this sidebar.', style={'paddingLeft': '1em', 'paddingRight': '1em'}),

        html.H6('3. Submit your analysis', style={'paddingTop': '1.2em'}),
        html.Div('Analysis results will be shown in the display area to the right.', style={'paddingLeft': '1em', 'paddingRight': '1em'}),

    ]),

    components.button(ids.navbar_upload__go_to_upload__button, 'Upload >'),
])
