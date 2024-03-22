from dash import dcc, html
from plotly.express.colors import sample_colorscale

from layout import components, ids, styles
import config

heatmap_colors = {
    'YlOrRd': 'Warm',
    'Hot_r': 'Hot',
    'Reds': 'Red',
    'Greens': 'Green',
    'Blues': 'Blue',
    'Greys': 'Gray',
}

clustergram_options = (
    html.Div(id=ids.navbar_analyze_clustergram__options__div, children=[

        components.dropdown_label('Group By (Method)'),
        components.multi_dropdown(ids.navbar_analyze_clustergram__grouping_columns__dropdown, style=styles.dropdown_with_related_element_below),
        components.grouping_method_dropdown(ids.navbar_analyze_clustergram__grouping_method__dropdown),

        components.dropdown_label('Label By'),
        components.multi_dropdown(ids.navbar_analyze_clustergram__labeling_columns__dropdown, style=styles.dropdown_with_related_element_below),

        dcc.Checklist(
            id=ids.navbar_analyze_clustergram__labeling_method__checklist,
            style=styles.checklist,
            options={'text_and_color': ' Color-Code Labels'},
            value=['text_and_color']
        ),

        components.dropdown_label('Heatmap Coloring'),
        dcc.Dropdown(
            id=ids.navbar_analyze_clustergram__heatmap_colors__dropdown,
            style=styles.dropdown,
            value=list(heatmap_colors.keys())[0],
            clearable=False,
            options=heatmap_colors
        ),

        components.font_size_selector(ids.navbar_analyze_clustergram__font_size__input),

        components.button(ids.navbar_analyze_clustergram__submit__button, 'Submit'),
    ])
)


def generate_css_for_gradient_dropdown(dropdown_id, color_dict):
    with open('layout/navbar/analyze/heatmap_colors_template.css', 'r') as template_css_file:
        css_template = template_css_file.read()

    n = 0
    write_string = ''
    for key in list(color_dict.keys()):
        sample_colors = sample_colorscale(key, [0.1 * i for i in range(10 + 1)])
        sample_colors.reverse()
        gradient = ','.join(sample_colors)
        text_color = sample_colorscale(key, [0.0])[0]
        n += 1

        write_string += (
            css_template
            .replace('_/*dropdown_class_name*/', dropdown_id)
            .replace('0/*nth-child*/', str(n))
            .replace('/*color_name*/', key)
            .replace('none/*background-image*/', f'linear-gradient(to right, {gradient})')
            .replace('black/*color*/', text_color)
        )

    with open('assets/heatmap_colors.css', 'w') as css_file:
        css_file.write(write_string)


if not config.bundled_mode:
    generate_css_for_gradient_dropdown(ids.navbar_analyze_clustergram__heatmap_colors__dropdown, heatmap_colors)
