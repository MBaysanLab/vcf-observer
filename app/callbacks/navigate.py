from dash.dependencies import Input, Output, State

from dash_app import app
import config
from layout import ids


@app.callback(
    (Output(ids.navbar_analyze_venn__options__div, 'hidden'),
     Output(ids.display_analyze__venn_display__div, 'hidden')),

    (Output(ids.navbar_analyze_clustergram__options__div, 'hidden'),
     Output(ids.display_analyze__clustergram_display__div, 'hidden')),

    (Output(ids.navbar_analyze_prerec__options__div, 'hidden'),
     Output(ids.display_analyze__prerec_display__div, 'hidden')),

    (Output(ids.navbar_analyze_summary__options__div, 'hidden'),
     Output(ids.display_analyze__summary_display__div, 'hidden')),

    Input(ids.navbar_analyze_analyze__analysis_type__radio_items, 'value'),
)
def update_analysis(selected_tab):
    venn_hidden = True
    clustergram_hidden = True
    prerec_hidden = True
    summary_hidden = True

    if selected_tab == 'venn':
        venn_hidden = False

    if selected_tab == 'clustergram':
        clustergram_hidden = False

    if selected_tab == 'prerec':
        prerec_hidden = False

    if selected_tab == 'summary':
        summary_hidden = False

    return (
        *((venn_hidden,) * 2),
        *((clustergram_hidden,) * 2),
        *((prerec_hidden,) * 2),
        *((summary_hidden,) * 2),
    )


@app.callback(
    Output(ids.display_welcome__display__div, 'hidden'),
    Output(ids.display_upload__display__div, 'hidden'),
    Output(ids.display_analyze__display__div, 'hidden'),
    Input(ids.navbar_navbar__tabs__tabs, 'value'),
    prevent_initial_call=True,
)
def update_display(selected_tab):
    display_welcome_hidden = True
    display_uploaded_hidden = True
    display_results_hidden = True

    if selected_tab == 'tab-welcome':
        display_welcome_hidden = False

    if selected_tab == 'tab-upload':
        display_uploaded_hidden = False

    if selected_tab == 'tab-analyze':
        display_results_hidden = False

    return (
        display_welcome_hidden,
        display_uploaded_hidden,
        display_results_hidden,
    )


@app.callback(
    Output(ids.navbar_navbar__tabs__tabs, 'value'),

    Output(ids.navbar_upload__go_to_upload__button, 'n_clicks'),
    Output(ids.navbar_upload__go_to_analyze__button, 'n_clicks'),

    Output(ids.navbar_navbar__first_visit_for_tabs__store, 'data'),

    Input(ids.navbar_upload__go_to_upload__button, 'n_clicks'),
    Input(ids.navbar_upload__go_to_analyze__button, 'n_clicks'),

    State(ids.navbar_navbar__first_visit_for_tabs__store, 'data'),
)
def button_navigation(upload, analyze, first_visit):
    if first_visit is None:
        selected_tab = 'tab-welcome'
    else:
        selected_tab = 'tab-upload'

        if config.auto_submit:
            selected_tab = 'tab-analyze'

    if upload:
        selected_tab = 'tab-upload'

    if analyze:
        selected_tab = 'tab-analyze'

    return (
        selected_tab,
        0, 0,
        'not_first_visit',
    )


@app.callback(
    Output(ids.navbar_upload__go_to_upload__button, 'children'),
    Output(ids.navbar_upload__go_to_analyze__button, 'children'),

    Output(ids.navbar_analyze_venn__submit__button, 'children'),
    Output(ids.navbar_analyze_clustergram__submit__button, 'children'),
    Output(ids.navbar_analyze_prerec__submit__button, 'children'),
    Output(ids.navbar_analyze_summary__filename_submit__button, 'children'),
    Output(ids.navbar_analyze_summary__metadata_submit__button, 'children'),
    Output(ids.navbar_analyze_summary__raw_submit__button, 'children'),

    Output(ids.navbar_navbar__first_visit_for_buttons__store, 'data'),

    Input(ids.navbar_analyze_venn__submit__button, 'n_clicks'),
    Input(ids.navbar_analyze_clustergram__submit__button, 'n_clicks'),
    Input(ids.navbar_analyze_prerec__submit__button, 'n_clicks'),
    Input(ids.navbar_analyze_summary__filename_submit__button, 'n_clicks'),
    Input(ids.navbar_analyze_summary__metadata_submit__button, 'n_clicks'),
    Input(ids.navbar_analyze_summary__raw_submit__button, 'n_clicks'),

    State(ids.navbar_navbar__first_visit_for_buttons__store, 'data'),
)
def button_guide_text(_1, _2, _3, _4, _5, _6, first_visit):
    if first_visit is None:
        go_to_upload_text = 'Upload your VCFs >'
        go_to_analyze_text = 'Select analysis options >'
        submit_text = 'Submit your analysis >'
    else:
        go_to_upload_text = 'Upload >'
        go_to_analyze_text = 'Analyze >'
        submit_text = 'Submit'

    return (
        go_to_upload_text,
        go_to_analyze_text,
        *((submit_text,) * 6),
        'not_first_visit',
    )


@app.callback(
    Output(ids.navbar_analyze_summary__filename_options__div, 'hidden'),
    Output(ids.display_analyze__filename_summary_display__div, 'hidden'),
    Output(ids.navbar_analyze_summary__metadata_options__div, 'hidden'),
    Output(ids.display_analyze__metadata_summary_display__div, 'hidden'),
    Output(ids.navbar_analyze_summary__raw_options__div, 'hidden'),
    Output(ids.display_analyze__raw_summary_display__div, 'hidden'),

    Input(ids.navbar_analyze_summary__type__radio_items, 'value'),
)
def update_summary_type(summary_type):
    filename_hidden = True
    metadata_hidden = True
    raw_hidden = True

    if summary_type == 'filename':
        filename_hidden = False

    if summary_type == 'metadata':
        metadata_hidden = False

    if summary_type == 'raw':
        raw_hidden = False

    return (
        *((filename_hidden,) * 2),
        *((metadata_hidden,) * 2),
        *((raw_hidden,) * 2),
    )


@app.callback(
    Output(ids.navbar_analyze_summary__font_size__div, 'hidden'),
    Input(ids.navbar_analyze_summary__filename_visualization__div, 'value'),
)
def update_font_size_selector_visibility(visualization_type):
    font_size_selector_hidden = True

    if visualization_type == 'graph':
        font_size_selector_hidden = False

    return font_size_selector_hidden
