from dash import dcc, html

from layout import components, ids, styles

venn_options = (
    html.Div(id=ids.navbar_analyze_venn__options__div, children=[

        components.dropdown_label('Group By (Method)'),
        components.multi_dropdown(ids.navbar_analyze_venn__grouping_columns__dropdown, style=styles.dropdown_with_related_element_below),
        components.grouping_method_dropdown(ids.navbar_analyze_venn__grouping_method__dropdown),

        dcc.Checklist(
            id=ids.navbar_analyze_venn__prefer_pseudovenn__checklist,
            style=styles.checklist,
            options={'prefer_pseudovenn': ' Use pseudo-Venn for n=6'},
            value=[]
        ),

        components.font_size_selector(ids.navbar_analyze_venn__font_size__input, default_value=8),

        components.button(ids.navbar_analyze_venn__submit__button, 'Submit'),

        html.Div([
            components.download_button(ids.navbar_analyze_venn__figure_download__button, 'Download Figure'),
            components.download_button_secondary(ids.navbar_analyze_venn__sites_download__button, 'Download Common Sites'),

            dcc.Download(id=ids.navbar_analyze_venn__figure_download__download),
            dcc.Download(id=ids.navbar_analyze_venn__sites_download__download),
        ])

    ])
)
