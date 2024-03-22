import dash
from dash.dependencies import Input, Output, State

import config
from dash_app import app
from layout import ids


@app.callback(
    Output(ids.navbar_analyze_clustergram__submit__button, 'n_clicks'),
    Output(ids.navbar_analyze_prerec__submit__button, 'n_clicks'),
    Output(ids.navbar_analyze_summary__filename_submit__button, 'n_clicks'),
    Output(ids.navbar_analyze_summary__metadata_submit__button, 'n_clicks'),
    Output(ids.navbar_analyze_summary__raw_submit__button, 'n_clicks'),
    Output(ids.navbar_analyze_venn__submit__button, 'n_clicks'),

    Input(ids.navbar_upload__compare_set_valid__store, 'data'),
    Input(ids.navbar_upload__golden_set_valid__store, 'data'),
    Input(ids.navbar_upload__metadata_valid__store, 'data'),

    Input(ids.navbar_analyze_venn__grouping_columns__dropdown, 'options'),
    Input(ids.navbar_analyze_clustergram__grouping_columns__dropdown, 'options'),
    Input(ids.navbar_analyze_prerec__grouping_columns__dropdown, 'options'),
    Input(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'options'),
)
def auto_submit_all_figures(
        compare_set_validity, golden_set_validity, metadata_validity,
        _1, _2, _3, _4,
):
    if config.auto_submit:
        if (
            compare_set_validity == 'compare_set_is_valid' and
            golden_set_validity == 'golden_set_is_valid' and
            metadata_validity == 'metadata_is_valid'
        ):
            return (-1,) * 6
        else:
            return (dash.no_update,) * 6
    else:
        return (dash.no_update,) * 6
