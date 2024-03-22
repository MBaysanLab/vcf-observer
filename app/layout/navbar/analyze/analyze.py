import os

from dash import dcc, html

import config
from layout.navbar.analyze.venn import venn_options
from layout.navbar.analyze.clustergram import clustergram_options
from layout.navbar.analyze.prerec import prerec_options
from layout.navbar.analyze.summary import summary_options

from layout import ids, styles

BED_dict = {
    'none': 'Genomic regions: None',
    'custom': 'Genomic regions: Custom',
}
if not config.bundled_mode:
    BED_dict = {**BED_dict, **{filename: filename[:-4] for filename in os.listdir('../BED Files') if filename[0] != '.'}}

analyze_tab = (
    dcc.Tab(label='Analyze', value='tab-analyze', style=styles.tab, selected_style=styles.tab_selected, children=[
        html.H6('Analysis Type'),
        dcc.RadioItems(
            id=ids.navbar_analyze_analyze__analysis_type__radio_items,
            style=styles.radio_items,
            labelStyle={'display': 'block'},
            options={
                'summary': ' Data Summary',
                'venn': ' Venn Diagram',
                'clustergram': ' Clustergram',
                'prerec': ' Precision-Recall Plot',
            },
            value='summary'
        ),

        html.Div([
            venn_options,
            clustergram_options,
            prerec_options,
            summary_options
        ]),

        html.Div(style={'marginTop': '-1em', 'clear': 'both', 'marginBottom': '1em'}, children=[html.Br(), html.Div(
            style={
                'backgroundColor': styles.dark_gray,
                'borderRadius': '0.8em',
                'padding': '0.6em',
            },
            children=[
                dcc.Checklist(
                    id=ids.navbar_analyze_analyze__filter_pass__checklist,
                    style=styles.checklist,
                    labelStyle={'paddingRight': '1em'},
                    options={'filter_pass': ' Apply PASS filter'},
                    value=['']
                ),
                dcc.Dropdown(
                    id=ids.navbar_analyze_analyze__genomic_regions__dropdown,
                    style=styles.dropdown_with_related_element_below,
                    clearable=False,
                    value='none',
                    options=BED_dict
                ),
                dcc.RadioItems(
                    id=ids.navbar_analyze_analyze__inside_outside_regions__radio_items,
                    style={**styles.checklist, 'marginBottom': '0.4em'},
                    labelStyle={'paddingRight': '1em'},
                    options={
                        'inside_regions': ' Inside of regions',
                        'outside_regions': ' Outside of regions',
                    },
                    value='inside_regions',
                )
            ])
        ])
    ])
)
