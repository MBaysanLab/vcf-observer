import os

import pandas as pd

from dash import html
from dash.dependencies import Input, Output

from dash_app import app
from data.cache import (
    set_compare_set_cache_as_df,
    set_golden_set_cache_as_df,
    set_metadata_cache_as_df,
    set_regions_cache_as_df,
)
from callbacks.helpers import normalize_upload_filename
from data.retrieval import get_uploaded_data
from layout import ids, styles


@app.callback(
    Output(ids.navbar_upload__compare_set_upload_result__div, 'children'),
    Output(ids.display_upload__compare_set_summary_card__div, 'children'),
    Output(ids.navbar_upload__compare_set_valid__store, 'data'),

    Input(ids.navbar_upload__compare_set__upload, 'filename'),
    Input(ids.navbar_upload__compare_set__upload, 'contents'),

    Input(ids.navbar_navbar__session_id__store, 'data'),
)
def on_compare_set_upload(filenames, contents, session_id):
    filenames = normalize_upload_filename(filenames)

    compare_set = None
    compare_set_valid = 'compare_set_is_invalid'
    exception = None
    if filenames:
        try:
            compare_set = set_compare_set_cache_as_df(session_id, filenames, contents)
            compare_set_valid = 'compare_set_is_valid'

        except Exception as e:
            exception = e

    result = vcf_upload_result(filenames, exception)
    summary_card = generate_compare_set_summary_card(compare_set, exception)

    return result, summary_card, compare_set_valid


@app.callback(
    Output(ids.navbar_upload__golden_set_upload_result__div, 'children'),
    Output(ids.display_upload__golden_set_summary_card__div, 'children'),
    Output(ids.navbar_upload__golden_set_valid__store, 'data'),

    Input(ids.navbar_upload__golden_set__upload, 'filename'),
    Input(ids.navbar_upload__golden_set__upload, 'contents'),
    Input(ids.navbar_navbar__session_id__store, 'data'),
)
def on_golden_set_upload(filenames, contents, session_id):
    filenames = normalize_upload_filename(filenames)

    golden_set = None
    golden_set_valid = 'golden_set_is_invalid'
    exception = None
    if filenames:
        try:
            golden_set = set_golden_set_cache_as_df(session_id, filenames, contents)
            golden_set_valid = 'golden_set_is_valid'
        except Exception as e:
            exception = e

    result = vcf_upload_result(filenames, exception)
    summary_card = generate_golden_set_summary_card(golden_set, exception)

    return result, summary_card, golden_set_valid


@app.callback(
    Output(ids.navbar_upload__metadata_upload_result__div, 'children'),
    Output(ids.display_upload__metadata_summary_card__div, 'children'),

    Output(ids.navbar_upload__metadata_valid__store, 'data'),

    Input(ids.navbar_upload__metadata__upload, 'filename'),
    Input(ids.navbar_upload__metadata__upload, 'contents'),
    Input(ids.navbar_upload__compare_set_valid__store, 'data'),

    Input(ids.navbar_navbar__session_id__store, 'data'),
)
def on_metadata_upload(metadata_filenames, metadata_contents, compare_set_valid, session_id):
    metadata_filenames = normalize_upload_filename(metadata_filenames)

    (
        (compare_set,),
        _,
        _
    ) = get_uploaded_data(session_id, compare_set_valid=compare_set_valid)

    if compare_set is None:
        compare_set_filenames = []
    else:
        compare_set_filenames = compare_set['FILENAME'].unique().tolist()

    missing_filenames = []
    metadata = None
    metadata_valid = 'metadata_is_invalid'
    exception = None
    if metadata_filenames:
        try:
            metadata = set_metadata_cache_as_df(session_id, metadata_filenames, metadata_contents, compare_set_filenames)
            missing_filenames = missing_metadata(metadata, compare_set_filenames)

            if not missing_filenames:
                metadata_valid = 'metadata_is_valid'
        except Exception as e:
            exception = e

    result = csv_upload_result(metadata_filenames, exception)
    summary_card = generate_metadata_summary_card(metadata, metadata_filenames, missing_filenames, exception)

    return result, summary_card, metadata_valid


@app.callback(
    (Output(ids.navbar_analyze_venn__grouping_columns__dropdown, 'options'),
     Output(ids.navbar_analyze_venn__grouping_columns__dropdown, 'value')),
    (Output(ids.navbar_analyze_clustergram__grouping_columns__dropdown, 'options'),
     Output(ids.navbar_analyze_clustergram__grouping_columns__dropdown, 'value')),
    (Output(ids.navbar_analyze_prerec__grouping_columns__dropdown, 'options'),
     Output(ids.navbar_analyze_prerec__grouping_columns__dropdown, 'value')),
    (Output(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'options'),
     Output(ids.navbar_analyze_summary__metadata_grouping_columns__dropdown, 'value')),

    Input(ids.navbar_upload__compare_set_valid__store, 'data'),
    Input(ids.navbar_upload__metadata_valid__store, 'data'),

    Input(ids.navbar_navbar__session_id__store, 'data'),
)
def on_complete_metadata_upload(compare_set_valid, metadata_valid, session_id):
    group_selection = []
    group_selection_value = []

    (
        (_, metadata),
        _,
        _
    ) = get_uploaded_data(session_id, compare_set_valid=compare_set_valid, metadata_valid=metadata_valid)

    if metadata is not None:
        group_selection = metadata.columns.values
        if len(group_selection) > 0:
            group_selection_value = [group_selection[0]]

    return (group_selection, group_selection_value) * 4


@app.callback(
    Output(ids.navbar_upload__regions_upload_result__div, 'children'),
    Output(ids.display_upload__regions_summary_card__div, 'children'),
    Output(ids.navbar_upload__regions_valid__store, 'data'),

    Input(ids.navbar_upload__regions__upload, 'filename'),
    Input(ids.navbar_upload__regions__upload, 'contents'),
    Input(ids.navbar_navbar__session_id__store, 'data'),
)
def on_regions_upload(filenames, contents, session_id):
    filenames = normalize_upload_filename(filenames)

    regions = None
    regions_valid = 'regions_is_invalid'
    exception = None
    if filenames:
        try:
            regions = set_regions_cache_as_df(session_id, filenames, contents)
            regions_valid = 'regions_is_valid'
        except Exception as e:
            exception = e

    result = bed_upload_result(filenames, exception)
    summary_card = generate_regions_summary_card(regions, filenames, exception)

    return result, summary_card, regions_valid


def upload_summary_card(title, status, body_items, counts_list=None, aggregate_after=5):
    body_items = filename_lister(body_items, aggregate_after=aggregate_after)

    if counts_list:
        counts_list = count_lister(counts_list, aggregate_after=aggregate_after)
    else:
        counts_list = [None] * len(body_items)

    return (
        html.Div(style=styles.upload_summary_card, children=[
            html.Div([
                html.H4(title, style={'display': 'inline-block'}),
                html.Div(status, style={'display': 'inline-block', 'paddingLeft': '1em'})
            ]),
            html.P(style={'paddingLeft': '1em', 'marginBottom': '0px', 'whiteSpace': 'pre-line'}, children=[
                html.Pre(html.Table(html.Tbody(
                    [
                        html.Tr([
                            html.Td(count, style={'textAlign': 'right', 'paddingRight': '1em'}) if count else None,
                            html.Td(body_item)
                        ])
                        for count, body_item in zip(counts_list, body_items)
                    ]
                )))
            ])
        ])
    )


def vcf_upload_result(filenames: list, e: Exception = None):

    if e:
        message = 'Errors encountered when processing files.'
    else:
        message = f'{len(filenames)} VCFs have been uploaded.'

        if len(filenames) == 0:
            message = 'No VCFs have been uploaded.'

        if len(filenames) == 1:
            message = '1 VCF has been uploaded.'

    return message


def csv_upload_result(filenames: list, e: Exception = None):
    if e:
        message = 'Errors encountered when processing files.'
    else:
        message = f'{len(filenames)} CSVs have been uploaded.'

        if len(filenames) == 0:
            message = 'No CSVs have been uploaded.'

        if len(filenames) == 1:
            message = '1 CSV has been uploaded.'

    return message


def bed_upload_result(filenames: list, e: Exception = None):
    if e:
        message = 'Errors encountered when processing files.'
    else:
        message = f'{len(filenames)} BEDs have been uploaded.'

        if len(filenames) == 0:
            message = 'No BEDs have been uploaded.'

        if len(filenames) == 1:
            message = '1 BED has been uploaded.'

    return message


def generate_compare_set_summary_card(compare_set: pd.DataFrame, e: Exception = None):
    if e:
        return upload_summary_card('Compare Set', 'An exception occurred:', [f'{e}'])

    if compare_set is None:
        status = 'Not uploaded.'
        filenames = ['> Required for analysis.']
        counts = []
    else:
        files = compare_set.groupby('FILENAME').size().sort_values(ascending=False)

        filenames = files.index.tolist()
        counts = files.tolist()

        status = [html.Pre(sum(counts), style={'display': 'inline'}), ' variants loaded.']

    return upload_summary_card('Compare Set', status, filenames, counts, aggregate_after=11)


def generate_golden_set_summary_card(golden_set: pd.DataFrame, e: Exception = None):
    if e:
        return upload_summary_card('Golden Set', 'An exception occurred:', [f'{e}'])

    if golden_set is None:
        status = 'Not uploaded.'
        filenames = [
            '> Required for benchmarking.',
            '> Precision and recall are calculated based on exact matches of variants.',
        ]
        counts = []
    else:
        files = golden_set.groupby('FILENAME').size().sort_values(ascending=False)

        filenames = files.index.tolist()
        counts = files.tolist()

        status = [html.Pre(sum(counts), style={'display': 'inline'}), ' variants loaded.']

    return upload_summary_card('Golden Set', status, filenames, counts, aggregate_after=3)


def generate_metadata_summary_card(metadata: pd.DataFrame, csv_filenames: list, files_not_in_metadata: list, e: Exception = None):
    if e:
        return upload_summary_card('Metadata', 'An exception occurred:', [f'{e}'])

    if csv_filenames:
        if files_not_in_metadata:
            status = 'Metadata missing for files below:'
            filenames = files_not_in_metadata
        else:
            status = 'Loaded following columns:'
            filenames = metadata.columns.values.tolist()
    else:
        status = 'Not uploaded.'
        filenames = [
            '> Required to dynamically group VCFs.',
            '> Must contain a column titled "FILENAME".',
            '> Must contain a row for each VCF in the compare set.',
        ]

    return upload_summary_card('Metadata', status, filenames, aggregate_after=4)


def generate_regions_summary_card(regions: pd.DataFrame, bed_filenames: list, e: Exception = None):
    if e:
        return upload_summary_card('Genomic Regions', 'An exception occurred:', [f'{e}'])

    if not bed_filenames:
        status = 'Not uploaded.'
        filenames = ['> Custom regions for filtering.']
    else:
        status = [html.Pre(len(regions), style={'display': 'inline'}), ' regions loaded.']
        filenames = bed_filenames

    return upload_summary_card('Genomic Regions', status, filenames, aggregate_after=3)


def filename_lister(filenames: list, aggregate_after: int) -> list:
    if len(filenames) > aggregate_after + 1:
        filenames[aggregate_after] = f'... and {len(filenames) - aggregate_after} more'
        filenames = filenames[:aggregate_after + 1]

    return filenames


def count_lister(counts: list, aggregate_after=11) -> list:
    if len(counts) > aggregate_after + 1:
        counts[aggregate_after] = sum(counts[aggregate_after:])
        counts = counts[:aggregate_after + 1]

    return list(map(str, counts))


def missing_metadata(metadata: pd.DataFrame, filenames_to_look_for: list):
    missing_filenames = []
    for filename in filenames_to_look_for:
        if filename not in metadata['FILENAME'].values:
            missing_filenames.append(filename)
    return missing_filenames
