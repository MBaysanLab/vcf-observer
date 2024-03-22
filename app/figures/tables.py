from datetime import datetime

import numpy as np
import pandas as pd
from dash import dash_table

from figures.helpers import _sets_from_files, _extract_single_element_list, _str_to_tuple, _clean_tuple


def df_to_table(
        input_df: pd.DataFrame,
        numeric_index: bool = True,
        return_updated_df: bool = False
) -> (dash_table.DataTable, pd.DataFrame):
    df = (
        input_df.reset_index()
                .rename(columns={'index': ''})
    )

    if numeric_index:
        df[''] = pd.Series(df[''].values + 1)

        if len(df.index) > 0 and len(df.columns) > 1 and df.iloc[-1, 1] == 'TOTAL':
            df[''] = df[''][:-1]

        header_column_color = {}
        default_text_alignment = 'left'
    else:
        header_column_color = {'backgroundColor': '#fafafa'}
        default_text_alignment = 'right'

    if isinstance(df.columns, pd.MultiIndex):
        columns = [{'name': list(column), 'id': _clean_tuple(column)} for column in df.columns.values]

        df.columns = [_clean_tuple(column) for column in df.columns.values]

        merge_duplicate_headers = True
        style_header = {'textAlign': 'center'}
    else:
        columns = [{'name': column, 'id': column} for column in df.columns]

        merge_duplicate_headers = False
        style_header = {}

    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=columns,
        cell_selectable=False,
        merge_duplicate_headers=merge_duplicate_headers,
        style_header=style_header,
        style_cell={'textAlign': default_text_alignment},
        style_cell_conditional=[
            {
                'if': {'column_id': df.columns.values[0]},
                'textAlign': 'right',
                'minWidth': 'fit-content',
                'width': '1.2em',
                **header_column_color,
            },
            {
                'if': {'column_id': df.columns.values[-1]},
                'textAlign': 'right',
            },
        ]
    )

    if return_updated_df:
        return table, df
    else:
        return table


def grouped_variant_counts(
        data: pd.DataFrame,
        metadata: pd.DataFrame,
        grouping_columns: list,
        grouping_method: str,
        pivoting_columns: list = (),
        return_updated_df: bool = False,
) -> (dash_table.DataTable, pd.DataFrame):
    comparing_column = 'KEY'
    counting_column = '# of Variants'

    groups = metadata.groupby(_extract_single_element_list(grouping_columns))

    sets_labels = list(groups.groups.keys())
    sets_files = [groups.get_group(set_label)['FILENAME'] for set_label in sets_labels]
    sets_labels = [_str_to_tuple(set_labels) for set_labels in sets_labels]
    sets_labels_transposed = np.array(sets_labels).T

    sets = _sets_from_files(data, sets_files, grouping_method, comparing_column)

    data_dict = {}
    for grouping_column, sets_label in zip(grouping_columns, sets_labels_transposed):
        data_dict[grouping_column] = sets_label

    data_dict[counting_column] = [len(each_set) for each_set in sets]

    df = pd.DataFrame(data_dict)

    if pivoting_columns:
        grouping_columns = [grouping_column for grouping_column in grouping_columns if
                            grouping_column not in pivoting_columns]
        grouping_columns = None if not grouping_columns else grouping_columns
        df = df.pivot(index=grouping_columns, columns=pivoting_columns, values=counting_column)

        if isinstance(df.index, pd.MultiIndex):
            df['new_index'] = [_clean_tuple(row_label) for row_label in df.index]
            df = df.set_index('new_index')

        df_with_totals = _calculate_totals_2d(df)

        table, df_table = df_to_table(df_with_totals, numeric_index=False, return_updated_df=True)
    else:
        df_with_total = _calculate_totals_1d(df, counting_column, grouping_columns)

        table, df_table = df_to_table(df_with_total, return_updated_df=True)

    if return_updated_df:
        return table, df_table
    else:
        return table


def _calculate_totals_1d(df: pd.DataFrame, counting_column: str, grouping_columns: list) -> pd.DataFrame:
    total_count = sum(map(lambda x: x[0], df[[counting_column]].values))
    df_with_total = pd.concat(
        [
            df,
            pd.DataFrame({grouping_columns[0]: ['TOTAL'], counting_column: [total_count]})
        ],
        ignore_index=True
    )
    return df_with_total


def _calculate_totals_2d(df: pd.DataFrame) -> pd.DataFrame:
    row_totals = [int(np.nansum(row)) for row in df.itertuples(index=False)]
    df_with_row_totals = df.copy()
    df_with_row_totals['TOTAL'] = row_totals

    col_totals = [[col_values.sum()] for _, col_values in df_with_row_totals.items()]
    df_with_totals = pd.concat([
        df_with_row_totals,
        pd.DataFrame(dict(zip(df_with_row_totals.columns.values, col_totals)), index=['TOTAL'])
    ])
    return df_with_totals


def df_to_csv(df: pd.DataFrame) -> str:
    csv_str = ','.join(df.columns) + '\n'

    row_strs = []
    for row in df.itertuples(index=False):
        row_values = map(lambda x: str(x), row)
        row_strs.append(','.join(row_values) + '\n')

    csv_str += ''.join(row_strs)

    return csv_str


def variant_df_to_vcf(input_df: pd.DataFrame) -> str:  # Expected columns: 'CHROM', 'POS', 'REF', 'ALT', 'FILTER'
    input_df['FILTER'] = input_df['FILTER_PASS'].apply(lambda filter_value: 'PASS' if filter_value else '.')
    processed_df = input_df.drop(columns=['FILTER_PASS'])

    processed_df['ID'] = '.'
    processed_df['QUAL'] = '.'
    processed_df['INFO'] = '.'

    vcf_df = processed_df[['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']]

    vcf_lines = [
        '##fileformat=VCFv4.3',
        '##fileDate=' + datetime.now().strftime('%Y%m%d'),
        '##source=VCFObserver',
        '#' + '\t'.join(vcf_df.columns)
    ]

    for row in vcf_df.itertuples(index=False):
        row_values = map(lambda x: str(x), row)
        vcf_lines.append('\t'.join(row_values))

    vcf_str = '\n'.join(vcf_lines) + '\n'

    return vcf_str
