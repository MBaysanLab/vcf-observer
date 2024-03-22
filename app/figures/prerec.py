import pandas as pd
from plotly import express as px

from figures.helpers import (
    _extract_single_element_list, _str_to_tuple,
    _corresponding_labels, _clean_tuple,
    _sets_from_files,
    _intersection_size
)


def precision_recall_plot(
        data: pd.DataFrame,
        validation_data: pd.DataFrame,
        metadata: pd.DataFrame,
        grouping_columns: list,
        grouping_method: str,
        labeling_columns: list,
        coloring_columns: list,
        shaping_columns: list,
        font_size: float = 12.0
) -> px.scatter:
    comparing_column = 'KEY'

    groups = metadata.groupby(_extract_single_element_list(grouping_columns))

    sets_labels = list(groups.groups.keys())
    sets_files = [groups.get_group(set_label)['FILENAME'] for set_label in sets_labels]
    sets_labels = [_str_to_tuple(set_labels) for set_labels in sets_labels]

    if len(labeling_columns) == 0:
        clean_labels = [' ' for i in range(groups.ngroups)]
    else:
        clean_labels = _corresponding_labels(sets_labels, grouping_columns, labeling_columns, metadata)
        clean_labels = [_clean_tuple(clean_label) for clean_label in clean_labels]

    coloring_labels = _corresponding_labels(sets_labels, grouping_columns, coloring_columns, metadata)
    coloring_labels = [_clean_tuple(coloring_label) for coloring_label in coloring_labels]

    shaping_labels = _corresponding_labels(sets_labels, grouping_columns, shaping_columns, metadata)
    shaping_labels = [_clean_tuple(shaping_label) for shaping_label in shaping_labels]

    sets = _sets_from_files(data, sets_files, grouping_method, comparing_column)
    validation_set = set(validation_data[comparing_column])

    precision_recall_data = []
    for i in range(len(sets)):
        for j in range(len(sets)):
            precision_recall_data.append({
                'Labels': clean_labels[i],
                'Colors': coloring_labels[i],
                'Shapes': shaping_labels[i],
                'Precision': _precision(sets[i], validation_set),
                'Recall': _recall(sets[i], validation_set)
            })

    precision_recall_df = pd.DataFrame(precision_recall_data)

    color_selector = 'Colors'
    if len(coloring_columns) == 0:
        color_selector = None

    shape_selector = 'Shapes'
    if len(shaping_columns) == 0:
        shape_selector = None

    figure = px.scatter(
        precision_recall_df,
        x='Precision',
        y='Recall',
        text='Labels',
        color=color_selector,
        symbol=shape_selector,
        hover_data=['Labels'],
        height=800
    )

    figure.layout['title'] = {
        'text': 'Precision-Recall Plot' + (f' Grouped by {_clean_tuple(grouping_columns)}' if grouping_columns != ['FILENAME'] else ''),
        'x': 0.5,
        'y': 0.975,
    }

    figure.update_layout(font={'size': font_size})

    figure.update_xaxes(range=[0, 1])
    figure.update_yaxes(range=[0, 1])

    figure.update_traces(
        hovertemplate='%{customdata[0]}',
        marker_size=20,
        textposition='bottom right'
    )

    return figure


def _precision(retrieved_set: set, relevant_set: set) -> float:
    if len(retrieved_set) == 0:
        return 0.0

    correct_findings = _intersection_size(retrieved_set, relevant_set)
    precision_value = correct_findings / len(retrieved_set)
    return precision_value


def _recall(retrieved_set: set, relevant_set: set) -> float:
    if len(relevant_set) == 0:
        return 0.0

    correct_findings = _intersection_size(retrieved_set, relevant_set)
    recall_value = correct_findings / len(relevant_set)
    return recall_value
