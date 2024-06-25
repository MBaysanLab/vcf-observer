import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State

from dash_app import app
from callbacks.helpers import normalize_dropdown_value, placeholder
from data.retrieval import get_uploaded_data
from data.file_readers import read_local_bed_files
from data.cache import set_filename_download_cache, set_metadata_download_cache, set_raw_download_cache
from figures.histogram import histogram
from figures.tables import df_to_table, df_to_csv, grouped_variant_counts
from layout import ids


@app.callback(
    Output(ids.navbar_analyze_summary__metadata_pivoting_columns__dropdown, 'options'),
    Output(ids.navbar_analyze_summary__metadata_pivoting_columns__dropdown, 'value'),

    Input(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'value'),
    Input(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'options'),
)
def on_select_summary_group(grouping_props, grouping_options):
    grouping_props = normalize_dropdown_value(grouping_props)
    return grouping_props, grouping_props[(len(grouping_props) + 1) // 2:] if len(grouping_props) > 1 else []


@app.callback(
    Output(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'disabled'),
    Output(ids.navbar_analyze_summary__metadata_pivoting_columns__dropdown, 'disabled'),

    Input(ids.navbar_analyze_summary__metadata_all__checklist, 'value'),
)
def on_all_select(all_selection):
    group_selection_disabled = False

    if all_selection == ['all']:
        group_selection_disabled = True

    return group_selection_disabled, group_selection_disabled


@app.callback(
    Output(ids.display_analyze__filename_summary_display__div, 'children'),
    Output(ids.navbar_analyze_summary__filename_download__button, 'hidden'),

    Input(ids.navbar_analyze_summary__filename_submit__button, 'n_clicks'),

    Input(ids.navbar_navbar__session_id__store, 'data'),

    State(ids.navbar_analyze_summary__filename_set__dropdown, 'value'),
    State(ids.navbar_analyze_summary__filename_visualization__div, 'value'),
    State(ids.navbar_analyze_summary__font_size__input, 'value'),

    State(ids.navbar_analyze_analyze__filter_pass__checklist, 'value'),
    State(ids.navbar_analyze_analyze__genomic_regions__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__inside_outside_regions__radio_items, 'value'),
    State(ids.navbar_analyze_analyze__on_chromosome__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__variant_type__dropdown, 'value'),

    State(ids.navbar_upload__compare_set_valid__store, 'data'),
    State(ids.navbar_upload__golden_set_valid__store, 'data'),
    State(ids.navbar_upload__regions_valid__store, 'data'),
)
def on_request_filename_summary(
        n_clicks, session_id,
        set_selection, visualisation_selection, font_size,
        filter_options, genomic_regions, inside_outside_regions, on_chromosome, variant_type,
        compare_set_valid, golden_set_valid, regions_valid
):
    results = []
    set_filename_download_cache(session_id, pd.DataFrame())
    download_hidden = True

    if n_clicks is None:
        return placeholder, download_hidden

    if set_selection == 'compare_set':
        (
            (data,),
            notices,
            any_invalidity
        ) = get_uploaded_data(
            session_id,
            compare_set_valid=compare_set_valid,
            regions_valid=regions_valid,
            filter_options=filter_options,
            genomic_regions=genomic_regions,
            inside_outside_regions=inside_outside_regions,
            on_chromosome=on_chromosome,
            variant_type=variant_type,
        )

    if set_selection == 'golden_set':
        (
            (data,),
            notices,
            any_invalidity
        ) = get_uploaded_data(session_id, golden_set_valid=golden_set_valid)

    results += notices

    if not any_invalidity:
        data = data[['FILENAME', 'KEY']]
        total_count = len(data)

        grouped_data = (
            data.groupby('FILENAME')
                .count()
                .reset_index()
                .rename(columns={'FILENAME': 'Filename', 'KEY': '# of Variants'})
        )

        if set_selection == 'compare_set':
            title_set_indicator = 'Compare Set'

        if set_selection == 'golden_set':
            title_set_indicator = 'Golden Set'

        graph = dcc.Graph(style={'height': '90vh'}, figure=histogram(
            grouped_data,
            x='Filename',
            y='# of Variants',
            title=f'Variant Counts of {title_set_indicator} Files',
            font_size=font_size,
        ))

        grouped_data.loc[len(grouped_data.index)] = ('TOTAL', total_count)

        table, df = df_to_table(grouped_data, return_updated_df=True)

        if visualisation_selection == 'graph':
            results.append(graph)

        if visualisation_selection == 'table':
            results.append(table)

        set_filename_download_cache(session_id, df)

        download_hidden = False

    return results, download_hidden


@app.callback(
    Output(ids.display_analyze__metadata_summary_display__div, 'children'),
    Output(ids.navbar_analyze_summary__metadata_download__button, 'hidden'),

    Input(ids.navbar_analyze_summary__metadata_submit__button, 'n_clicks'),

    Input(ids.navbar_navbar__session_id__store, 'data'),

    State(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'options'),
    State(ids.navbar_analyze_summary__metadata_all__checklist, 'value'),

    State(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'value'),
    State(ids.navbar_analyze_summary__metadata_grouping_method__dropdown, 'value'),
    State(ids.navbar_analyze_summary__metadata_pivoting_columns__dropdown, 'value'),

    State(ids.navbar_analyze_analyze__filter_pass__checklist, 'value'),
    State(ids.navbar_analyze_analyze__genomic_regions__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__inside_outside_regions__radio_items, 'value'),
    State(ids.navbar_analyze_analyze__on_chromosome__dropdown, 'value'),
    State(ids.navbar_analyze_analyze__variant_type__dropdown, 'value'),

    State(ids.navbar_upload__compare_set_valid__store, 'data'),
    State(ids.navbar_upload__metadata_valid__store, 'data'),
    State(ids.navbar_upload__regions_valid__store, 'data'),
)
def on_request_metadata_summary(
        n_clicks, session_id,
        grouping_column_options, group_for_each,
        grouping_columns, grouping_method, pivoting_columns,
        filter_options, genomic_regions, inside_outside_regions, on_chromosome, variant_type,
        compare_set_valid, metadata_valid, regions_valid,
):
    grouping_column_options = normalize_dropdown_value(grouping_column_options)
    grouping_columns = normalize_dropdown_value(grouping_columns)
    pivoting_columns = normalize_dropdown_value(pivoting_columns)

    if not grouping_columns:
        grouping_columns = ['FILENAME']

    results = []
    set_metadata_download_cache(session_id, pd.DataFrame())
    download_hidden = True

    if n_clicks is None:
        return placeholder, download_hidden

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
            on_chromosome=on_chromosome,
            variant_type=variant_type,
        )

    results += notices

    if not any_invalidity:
        if group_for_each == ['all']:
            for group in grouping_column_options:
                results += [html.Div(
                    grouped_variant_counts(compare_set, metadata, [group], grouping_method),
                    style={'paddingBottom': '2em'}
                )]
        else:
            table, df = grouped_variant_counts(
                compare_set,
                metadata,
                grouping_columns,
                grouping_method,
                pivoting_columns,
                return_updated_df=True
            )

            set_metadata_download_cache(session_id, df)
            download_hidden = False

            results.append(table)

    return results, download_hidden


@app.callback(
    Output(ids.display_analyze__raw_summary_display__div, 'children'),
    Output(ids.navbar_analyze_summary__raw_download__button, 'hidden'),

    Input(ids.navbar_analyze_summary__raw_submit__button, 'n_clicks'),

    Input(ids.navbar_navbar__session_id__store, 'data'),

    State(ids.navbar_analyze_summary__raw_type__dropdown, 'value'),

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
def on_request_raw_summary(
        n_clicks, session_id, set_selection,
        filter_options, genomic_regions, inside_outside_regions, on_chromosome, variant_type,
        compare_set_valid, golden_set_valid, metadata_valid, regions_valid,
):
    results = []
    set_raw_download_cache(session_id, pd.DataFrame())
    download_hidden = True

    if n_clicks is None:
        return placeholder, download_hidden

    merge_reminder = None

    if set_selection == 'compare_set':
        (
            (data,),
            notices,
            any_invalidity
        ) = get_uploaded_data(
            session_id,
            compare_set_valid=compare_set_valid,
            regions_valid=regions_valid,
            filter_options=filter_options,
            genomic_regions=genomic_regions,
            inside_outside_regions=inside_outside_regions,
            on_chromosome=on_chromosome,
            variant_type=variant_type,
        )
        if data is not None and data.groupby('FILENAME').ngroups > 1:
            merge_reminder = html.P('All uploaded VCFs have been merged into a single table.')

    if set_selection == 'golden_set':
        (
            (data,),
            notices,
            any_invalidity
        ) = get_uploaded_data(session_id, golden_set_valid=golden_set_valid)
        if data is not None and data.groupby('FILENAME').ngroups > 1:
            merge_reminder = html.P('All uploaded VCFs have been merged into a single table.')

    if set_selection == 'metadata':
        (
            (data,),
            notices,
            any_invalidity
        ) = get_uploaded_data(session_id, metadata_valid=metadata_valid)

    if set_selection == 'regions':
        if genomic_regions in ['none', 'custom']:
            (
                (data,),
                notices,
                any_invalidity
            ) = get_uploaded_data(session_id, regions_valid=regions_valid)

            results += notices
        else:
            data = read_local_bed_files(['../BED Files/' + genomic_regions])
            any_invalidity = False

    results += notices

    if not any_invalidity:
        row_truncate_limit = 100_000
        if len(data) > row_truncate_limit:
            results += [html.P(f'Only the first {row_truncate_limit} rows are shown.')]
        table, updated_data = df_to_table(data[:row_truncate_limit], return_updated_df=True)

        set_raw_download_cache(session_id, updated_data)
        download_hidden = False

        results += [merge_reminder, table]

    return results, download_hidden
