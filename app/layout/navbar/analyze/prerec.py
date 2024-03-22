from dash import html
from layout import components, ids, styles

prerec_options = (
    html.Div(id=ids.navbar_analyze_prerec__options__div, children=[

        components.dropdown_label('Group By (Method)'),
        components.multi_dropdown(ids.navbar_analyze_prerec__grouping_columns__dropdown, style=styles.dropdown_with_related_element_below),
        components.grouping_method_dropdown(ids.navbar_analyze_prerec__grouping_method__dropdown),

        components.dropdown_label('Label By'),
        components.multi_dropdown(ids.navbar_analyze_prerec__labeling_columns__dropdown),

        components.dropdown_label('Set Point Colors On'),
        components.multi_dropdown(ids.navbar_analyze_prerec__coloring_columns__dropdown),

        components.dropdown_label('Set Point Shapes On'),
        components.multi_dropdown(ids.navbar_analyze_prerec__shaping_columns__dropdown),

        components.font_size_selector(ids.navbar_analyze_prerec__font_size__input),

        components.button(ids.navbar_analyze_prerec__submit__button, 'Submit'),
    ])
)
