import pandas as pd
from plotly import graph_objs as go
from plotly.colors import sequential, qualitative
from dash_bio import Clustergram

from figures.helpers import (
    _extract_single_element_list, _str_to_tuple,
    _corresponding_labels, _clean_tuple,
    _sets_from_files,
    _intersection_size, _union_size
)


def clustergram(
        data: pd.DataFrame,
        metadata: pd.DataFrame,
        grouping_columns: list,
        grouping_method: str,
        labeling_columns: list,
        labeling_method: str = 'text',
        heatmap_colors: list = sequential.YlOrRd_r,
        font_size: float = 12.0
) -> Clustergram:
    comparing_column = 'KEY'

    groups = metadata.groupby(_extract_single_element_list(grouping_columns))

    sets_labels = list(groups.groups.keys())
    sets_files = [groups.get_group(set_label)['FILENAME'] for set_label in sets_labels]
    sets_labels = [_str_to_tuple(set_labels) for set_labels in sets_labels]

    clean_labels = _corresponding_labels(sets_labels, grouping_columns, labeling_columns, metadata)
    clean_labels = [_clean_tuple(clean_label) for clean_label in clean_labels]

    if 'color' in labeling_method:
        unique_labels = dict.fromkeys(clean_labels)
        potential_colors = qualitative.Safe

        label_color_dict = {}
        for i, clean_label in enumerate(unique_labels.keys()):
            label_color_dict[clean_label] = potential_colors[i % len(potential_colors)]

        label_colors = [label_color_dict[clean_label] for clean_label in clean_labels]
    else:
        label_colors = None

    sets = _sets_from_files(data, sets_files, grouping_method, comparing_column)

    if len(sets) == 1:
        sets.append(sets[0])
        sets_labels.append((' ',))
        clean_labels.append('Only 1 group found')

    heatmap_data = []
    for i in range(len(sets)):
        for j in range(len(sets)):
            heatmap_data.append({
                'Set 1': sets_labels[i],
                'Set 2': sets_labels[j],
                'Jaccard': _jaccard_distance(sets[i], sets[j])
            })

    heatmap_df = pd.DataFrame(heatmap_data)
    pivoted_heatmap = heatmap_df.pivot(index='Set 1', columns='Set 2', values='Jaccard')

    figure = Clustergram(
        data=pivoted_heatmap,
        column_labels=clean_labels,
        row_labels=clean_labels,
        center_values=False,
        color_map=heatmap_colors,
        row_colors=label_colors,
        column_colors=label_colors,
        width=1000,
        height=800,
        tick_font={'size': font_size},
        annotation_font={'size': font_size},
    )

    if 'color' in labeling_method:
        _add_legend_to_clustergram(figure, label_color_dict, title=_clean_tuple(labeling_columns), font_size=font_size)

    figure.layout['title'] = {
        'text': 'Clustergram' + (f' Grouped by {_clean_tuple(grouping_columns)}' if grouping_columns != ['FILENAME'] else ''),
        'x': 0.5,
        'y': 0.95,
        'font': {'size': font_size},
    }

    return figure


def _jaccard_distance(a: set, b: set) -> float:
    union_size = _union_size(a, b)

    if union_size == 0:
        return 0.0

    return _intersection_size(a, b) / union_size


def _add_legend_to_clustergram(clustergram: Clustergram, label_color_dict: dict, title=None, font_size=12.0):
    clustergram.layout.showlegend = True
    for obj in clustergram.data:
        obj.showlegend = False

    clustergram.add_traces([
        go.Bar(
            name=key,
            x=[0],
            width=0,
            marker_color=label_color_dict[key],
            showlegend=True
        )
        for key in label_color_dict
    ])

    clustergram.update_layout(
        legend={
            'title': title,
            'itemclick': False,
            'itemdoubleclick': False,
            'x': -0.05,
            'y': 1.2,
            'font': {'size': font_size}
        }
    )
