from base64 import b64encode

from dash import html
from dash.dependencies import Input, Output, State

from dash_app import app
from figures.venn_figure import venn_diagram
from callbacks.helpers import normalize_dropdown_value, large_centered_text, placeholder
from data.retrieval import get_uploaded_data
from data.cache import set_venn_figure_download_cache, set_venn_sites_download_cache
from layout import ids


@app.callback(
    Output(ids.display_analyze__venn_display__div, 'children'),
    Output(ids.navbar_analyze_venn__figure_download__button, 'hidden'),
    Output(ids.navbar_analyze_venn__sites_download__button, 'hidden'),

    Input(ids.navbar_analyze_venn__submit__button, 'n_clicks'),

    Input(ids.navbar_navbar__session_id__store, 'data'),

    State(ids.navbar_analyze_venn__grouping_columns__dropdown, 'value'),
    State(ids.navbar_analyze_venn__grouping_method__dropdown, 'value'),
    State(ids.navbar_analyze_venn__prefer_pseudovenn__checklist, 'value'),
    State(ids.navbar_analyze_venn__font_size__input, 'value'),

    State(ids.navbar_analyze_analyze__filter_pass__checklist, 'value'),
    State(ids.navbar_analyze_analyze__genomic_regions__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__inside_outside_regions__radio_items, 'value'),

    State(ids.navbar_upload__compare_set_valid__store, 'data'),
    State(ids.navbar_upload__metadata_valid__store, 'data'),
    State(ids.navbar_upload__regions_valid__store, 'data'),
)
def on_request_venn(
        n_clicks, session_id,
        grouping_columns, grouping_method, prefer_pseudovenn, font_size,
        filter_options, genomic_regions, inside_outside_regions,
        compare_set_valid, metadata_valid, regions_valid,
):
    grouping_columns = normalize_dropdown_value(grouping_columns)
    if not grouping_columns:
        grouping_columns = ['FILENAME']

    results = []
    image_data = ''
    download_hidden = True
    set_venn_figure_download_cache(session_id, '')

    if n_clicks is None:
        return placeholder, download_hidden, download_hidden

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
        try:
            if prefer_pseudovenn == ['prefer_pseudovenn']:
                pseudovenn_preference = 'pseudovenn'
            else:
                pseudovenn_preference = 'venn'

            figure_image_bytes, intersection_sites = venn_diagram(
                compare_set,
                metadata,
                grouping_columns,
                grouping_method,
                pseudovenn_preference,
                font_size=font_size,
                return_intersection=True,
            )

            image_data = b64encode(figure_image_bytes.getvalue()).decode('utf-8')

            results += [html.Img(src=f'data:image/png;base64,{image_data}')]

            download_hidden = False
            set_venn_figure_download_cache(session_id, image_data)
            set_venn_sites_download_cache(session_id, intersection_sites)

        except ValueError as e:
            results += [large_centered_text(f'{e}')]

    return results, download_hidden, download_hidden
