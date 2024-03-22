from dash import dcc
from dash.dependencies import Input, Output, State

from dash_app import app
from callbacks.helpers import normalize_dropdown_value, placeholder
from data.retrieval import get_uploaded_data
from figures.clustergram import clustergram
from layout import ids


@app.callback(
    Output(ids.navbar_analyze_clustergram__labeling_columns__dropdown, 'options'),
    Output(ids.navbar_analyze_clustergram__labeling_columns__dropdown, 'value'),

    Input(ids.navbar_analyze_clustergram__grouping_columns__dropdown, 'value'),
    Input(ids.navbar_analyze_clustergram__grouping_columns__dropdown, 'options'),
)
def on_select_clustergram_group(grouping_props, grouping_options):
    grouping_props = normalize_dropdown_value(grouping_props)
    grouping_options = normalize_dropdown_value(grouping_options)

    if 'FILENAME' in grouping_props:
        return grouping_options, grouping_props
    else:
        return grouping_props, grouping_props


@app.callback(
    Output(ids.navbar_analyze_clustergram__heatmap_colors__dropdown, 'className'),
    Input(ids.navbar_analyze_clustergram__heatmap_colors__dropdown, 'value'),
)
def on_select_heatmap_color(heatmap_color):
    return f'dropdown-color-{heatmap_color}'


@app.callback(
    Output(ids.display_analyze__clustergram_display__div, 'children'),

    Input(ids.navbar_analyze_clustergram__submit__button, 'n_clicks'),

    Input(ids.navbar_navbar__session_id__store, 'data'),

    State(ids.navbar_analyze_clustergram__grouping_columns__dropdown, 'value'),
    State(ids.navbar_analyze_clustergram__grouping_method__dropdown, 'value'),
    State(ids.navbar_analyze_clustergram__labeling_columns__dropdown, 'value'),
    State(ids.navbar_analyze_clustergram__labeling_method__checklist, 'value'),
    State(ids.navbar_analyze_clustergram__heatmap_colors__dropdown, 'value'),
    State(ids.navbar_analyze_clustergram__font_size__input, 'value'),

    State(ids.navbar_analyze_analyze__filter_pass__checklist, 'value'),
    State(ids.navbar_analyze_analyze__genomic_regions__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__inside_outside_regions__radio_items, 'value'),

    State(ids.navbar_upload__compare_set_valid__store, 'data'),
    State(ids.navbar_upload__metadata_valid__store, 'data'),
    State(ids.navbar_upload__regions_valid__store, 'data'),
)
def on_request_clustergram(
        n_clicks, session_id,
        grouping_columns, grouping_method,
        labeling_columns, labeling_method,
        heatmap_colors, font_size,
        filter_options, genomic_regions, inside_outside_regions,
        compare_set_valid, metadata_valid, regions_valid,
):
    grouping_columns = normalize_dropdown_value(grouping_columns)
    labeling_columns = normalize_dropdown_value(labeling_columns)

    if not grouping_columns or 'FILENAME' in grouping_columns:
        grouping_columns = ['FILENAME']

    if labeling_method == ['text_and_color']:
        labeling_method = 'text color'
    else:
        labeling_method = 'text'

    results = []

    if n_clicks is None:
        return placeholder

    (
        (compare_set, metadata),
        notices,
        any_invalidity
    ) = get_uploaded_data(
        session_id,
        compare_set_valid=compare_set_valid,
        metadata_valid=metadata_valid,
        regions_valid=regions_valid,
        filter_options=filter_options,
        genomic_regions=genomic_regions,
        inside_outside_regions=inside_outside_regions,
    )

    results += notices

    if not any_invalidity:
        results += [dcc.Graph(figure=clustergram(
            compare_set,
            metadata,
            grouping_columns,
            grouping_method,
            labeling_columns,
            labeling_method,
            heatmap_colors,
            font_size=font_size,
        ))]

    return results
