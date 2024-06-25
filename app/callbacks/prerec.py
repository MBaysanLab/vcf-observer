from dash import dcc
from dash.dependencies import Input, Output, State

from dash_app import app
from callbacks.helpers import get_first_element, get_second_element, normalize_dropdown_value, placeholder
from data.retrieval import get_uploaded_data
from figures.prerec import precision_recall_plot
from layout import ids


@app.callback(
    Output(ids.display_analyze__prerec_display__div, 'children'),

    Input(ids.navbar_analyze_prerec__submit__button, 'n_clicks'),

    Input(ids.navbar_navbar__session_id__store, 'data'),

    State(ids.navbar_analyze_prerec__grouping_columns__dropdown, 'value'),
    State(ids.navbar_analyze_prerec__grouping_method__dropdown, 'value'),
    State(ids.navbar_analyze_prerec__labeling_columns__dropdown, 'value'),
    State(ids.navbar_analyze_prerec__coloring_columns__dropdown, 'value'),
    State(ids.navbar_analyze_prerec__shaping_columns__dropdown, 'value'),
    State(ids.navbar_analyze_prerec__font_size__input, 'value'),

    State(ids.navbar_analyze_analyze__filter_pass__checklist, 'value'),
    State(ids.navbar_analyze_analyze__genomic_regions__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__inside_outside_regions__radio_items, 'value'),
    State(ids.navbar_analyze_analyze__on_chromosome__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__variant_type__dropdown, 'value'),

    State(ids.navbar_upload__compare_set_valid__store, 'data'),
    State(ids.navbar_upload__golden_set_valid__store, 'data'),
    State(ids.navbar_upload__metadata_valid__store, 'data'),
    State(ids.navbar_upload__regions_valid__store, 'data'),
)
def on_request_prerec(
        n_clicks, session_id,
        grouping_columns, grouping_method,
        labeling_columns, coloring_columns, shaping_columns, font_size,
        filter_options, genomic_regions, inside_outside_regions, on_chromosome, variant_type,
        compare_set_valid, golden_set_valid, metadata_valid, regions_valid,
):
    grouping_columns = normalize_dropdown_value(grouping_columns)
    labeling_columns = normalize_dropdown_value(labeling_columns)
    coloring_columns = normalize_dropdown_value(coloring_columns)
    shaping_columns = normalize_dropdown_value(shaping_columns)

    if not grouping_columns or 'FILENAME' in grouping_columns:
        grouping_columns = ['FILENAME']

    results = []

    if n_clicks is None:
        return placeholder

    (
        (compare_set, golden_set, metadata),
        notices,
        any_invalidity
    ) = get_uploaded_data(
            session_id,
            compare_set_valid=compare_set_valid,
            golden_set_valid=golden_set_valid,
            metadata_valid=metadata_valid,
            regions_valid=regions_valid,
            filter_options=filter_options,
            genomic_regions=genomic_regions,
            inside_outside_regions=inside_outside_regions,
            on_chromosome=on_chromosome,
            variant_type=variant_type,
    )

    results += notices

    if not any_invalidity:
        results += [dcc.Graph(figure=precision_recall_plot(
            compare_set,
            golden_set,
            metadata,
            grouping_columns,
            grouping_method,
            labeling_columns,
            coloring_columns,
            shaping_columns,
            font_size=font_size
        ))]

    return results


@app.callback(
    Output(ids.navbar_analyze_prerec__labeling_columns__dropdown, 'options'),
    Output(ids.navbar_analyze_prerec__labeling_columns__dropdown, 'value'),
    Output(ids.navbar_analyze_prerec__coloring_columns__dropdown, 'options'),
    Output(ids.navbar_analyze_prerec__coloring_columns__dropdown, 'value'),
    Output(ids.navbar_analyze_prerec__shaping_columns__dropdown, 'options'),
    Output(ids.navbar_analyze_prerec__shaping_columns__dropdown, 'value'),

    Input(ids.navbar_analyze_prerec__grouping_columns__dropdown, 'value'),
    Input(ids.navbar_analyze_prerec__grouping_columns__dropdown, 'options'),
)
def on_select_prerec_group(grouping_values, grouping_options):
    grouping_values = normalize_dropdown_value(grouping_values)
    grouping_options = normalize_dropdown_value(grouping_options)

    if 'FILENAME' in grouping_values:
        return (
            grouping_options, grouping_values,
            grouping_options, get_first_element(grouping_options),
            grouping_options, get_second_element(grouping_options),
        )
    else:
        return (
            grouping_values, grouping_values,
            grouping_values, get_first_element(grouping_values),
            grouping_values, get_second_element(grouping_values)
        )
