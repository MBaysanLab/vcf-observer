from dash import dcc, html

from layout import components, ids, styles

filename_div = (
    html.Div(id=ids.navbar_analyze_summary__filename_options__div, children=[
        components.dropdown_label('Variant Counts For'),
        dcc.Dropdown(
            id=ids.navbar_analyze_summary__filename_set__dropdown,
            style=styles.dropdown,
            clearable=False,
            value='compare_set',
            options={
                'compare_set': 'Compare Set',
                'golden_set': 'Golden Set',
            }
        ),

        components.dropdown_label('Visualize With'),
        dcc.Dropdown(
            id=ids.navbar_analyze_summary__filename_visualization__div,
            style=styles.dropdown,
            clearable=False,
            value='graph',
            options={
                'graph': 'Graph',
                'table': 'Table',
            }
        ),

        components.font_size_selector(ids.navbar_analyze_summary__font_size__input, div_id=ids.navbar_analyze_summary__font_size__div),

        components.button(ids.navbar_analyze_summary__filename_submit__button, 'Submit'),

        html.Div([
            components.download_button(ids.navbar_analyze_summary__filename_download__button, 'Download Data'),

            dcc.Download(id=ids.navbar_analyze_summary__filename_download__download),
        ])
    ])
)

metadata_div = (
    html.Div(id=ids.navbar_analyze_summary__metadata_options__div, children=[
        components.dropdown_label('Group By (Method)'),
        components.multi_dropdown(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, style=styles.dropdown_with_related_element_below),
        components.grouping_method_dropdown(ids.navbar_analyze_summary__metadata_grouping_method__dropdown, style=styles.dropdown_with_related_element_below),

        dcc.Checklist(
            id=ids.navbar_analyze_summary__metadata_all__checklist,
            style=styles.checklist,
            options={'all': ' List Each Metadata Column'},
            value=['all']
        ),

        components.dropdown_label('Pivot On'),
        components.multi_dropdown(ids.navbar_analyze_summary__metadata_pivoting_columns__dropdown),

        components.button(ids.navbar_analyze_summary__metadata_submit__button, 'Submit'),

        html.Div([
            components.download_button(ids.navbar_analyze_summary__metadata_download__button, 'Download Data'),

            dcc.Download(id=ids.navbar_analyze_summary__metadata_download__download),
        ])
    ])
)

raw_div = (
    html.Div(id=ids.navbar_analyze_summary__raw_options__div, children=[
        components.dropdown_label('Show Raw Data Of'),
        dcc.Dropdown(
            id=ids.navbar_analyze_summary__raw_type__dropdown,
            style=styles.dropdown,
            clearable=False,
            value='compare_set',
            options={
                'compare_set': 'Compare Set',
                'golden_set': 'Golden Set',
                'metadata': 'Metadata',
                'regions': 'Genomic Regions',
            }
        ),

        components.button(ids.navbar_analyze_summary__raw_submit__button, 'Submit'),

        html.Div([
            components.download_button(ids.navbar_analyze_summary__raw_download__button, 'Download Data'),

            dcc.Download(id=ids.navbar_analyze_summary__raw_download__download),
        ])
    ])
)

summary_options = (
    html.Div(id=ids.navbar_analyze_summary__options__div, children=[
        html.H6('Summarization Type'),
        dcc.RadioItems(
            id=ids.navbar_analyze_summary__type__radio_items,
            style=styles.radio_items,
            labelStyle={'display': 'block'},
            value='filename',
            options={
                'filename': ' Filename-Based Variant Counts',
                'metadata': ' Metadata-Based Variant Counts',
                'raw': ' Raw Data',
            }
        ),

        filename_div,
        metadata_div,
        raw_div,
    ])
)
