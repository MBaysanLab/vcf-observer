from functools import reduce

import pandas as pd


def _intersection_size(a: set, *b: set) -> int:
    return len(a.intersection(*b))


def _union_size(a: set, *b: set) -> int:
    return len(a.union(*b))


def _extract_single_element_list(in_value) -> str:
    if isinstance(in_value, list) and len(in_value) == 1:
        return in_value[0]
    else:
        return in_value


def _str_to_tuple(in_value) -> tuple:
    if isinstance(in_value, tuple):
        return in_value
    elif isinstance(in_value, str):
        return tuple([in_value])
    else:
        raise ValueError(f'Expected tuple or str, received {type(in_value)}.' +
                         f'Value received: {in_value}')


def _clean_tuple(in_value) -> str:
    return ' & '.join(in_value)


def _corresponding_labels(
        sets_labels: list,
        grouping_columns: list,
        labeling_columns: list,
        metadata: pd.DataFrame
) -> list:
    return_labels = []

    if grouping_columns == ['FILENAME']:
        for set_labels in sets_labels:
            set_metadata = metadata.loc[metadata['FILENAME'] == set_labels[0]]

            return_label = []
            for labeling_column in labeling_columns:
                return_label.append(set_metadata[labeling_column].iloc[0])

            return_labels.append(return_label)
    else:
        for set_labels in sets_labels:

            return_label = []
            for i in range(len(grouping_columns)):
                if grouping_columns[i] in labeling_columns:
                    return_label.append(set_labels[i])

            return_labels.append(return_label)

    return return_labels


def _intersect_dfs(dfs: list, on=None) -> set:
    sets = list(map(lambda df: set(df[on]), dfs))
    return sets[0].intersection(*sets[1:])


def _sets_from_files(
        data: pd.DataFrame,
        sets_files: list,
        grouping_method: str,
        comparing_column: str
) -> list:
    sets = []
    for set_files in sets_files:
        set_variants = []
        for set_file in set_files:
            set_variants.append(data.loc[data['FILENAME'] == set_file, data.columns != 'FILENAME'])
        sets.append(set_variants)

    if grouping_method == 'union':
        for i in range(len(sets)):
            sets[i] = set(pd.concat(sets[i], ignore_index=True)[comparing_column])

    if grouping_method == 'inter':
        for i in range(len(sets)):
            sets[i] = _intersect_dfs(sets[i], on=comparing_column)

    if grouping_method == 'major':
        for i in range(len(sets)):
            all_rows = pd.concat(sets[i], ignore_index=True)
            row_counts = all_rows.value_counts(comparing_column)

            half_of_file_count = len(sets_files[i]) // 2
            majority_rows = row_counts[row_counts > half_of_file_count]
            majority_keys = majority_rows.index.to_list()

            sets[i] = set(
                all_rows[all_rows[comparing_column].isin(majority_keys)][comparing_column]
            )

    return sets
