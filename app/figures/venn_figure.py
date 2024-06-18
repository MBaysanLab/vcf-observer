from io import BytesIO

import pandas as pd
from matplotlib import pyplot as plt
from venn import pseudovenn, venn

from figures.helpers import _extract_single_element_list, _str_to_tuple, _clean_tuple, _sets_from_files, _intersect_dfs


def venn_diagram(
        data: pd.DataFrame,
        metadata: pd.DataFrame,
        grouping_columns: list,
        grouping_method: str,
        pseudovenn_preference: str = 'venn',
        font_size: float = 8.0,
        return_intersection: bool = False
) -> BytesIO:
    comparing_column = 'KEY'
    legend_loc = 'upper left'
    prefer_pseudovenn = pseudovenn_preference == 'pseudovenn'

    groups = metadata.groupby(_extract_single_element_list(grouping_columns))
    no_of_groups = groups.ngroups

    if no_of_groups not in (1, 2, 3, 4, 5, 6):
        raise ValueError(
            f'The number of groups selected from the VCF data must be 1, 2, 3, 4, 5, or 6.' +
            f'There are {no_of_groups} for the current grouping constraints.'
        )

    sets_labels = list(groups.groups.keys())
    sets_files = [groups.get_group(set_label)['FILENAME'] for set_label in sets_labels]
    sets_labels = [_str_to_tuple(set_labels) for set_labels in sets_labels]

    clean_labels = sets_labels[:]
    clean_labels = [_clean_tuple(clean_label) for clean_label in clean_labels]

    sets = _sets_from_files(data, sets_files, grouping_method, comparing_column)

    sets_dict = {
        clean_labels[i]: sets[i]
        for i in range(no_of_groups)
    }

    title_y = -0.01
    pseudovenn_prefix = ''

    if all(len(s) == 0 for s in sets_dict.values()):
        sets_dict = {', '.join(sets_dict.keys()): set()}
        no_of_groups = 1

    if no_of_groups == 1:
        _venn1(sets_dict, fontsize=font_size, legend_loc=legend_loc)

    elif no_of_groups == 6 and prefer_pseudovenn:
        pseudovenn(sets_dict, fontsize=font_size, legend_loc=legend_loc, fmt='{size:,} ({percentage:.1f}%)', hint_hidden=False)
        pseudovenn_prefix = 'Pseudo-'
        title_at_top_y = None
        title_y = title_at_top_y

    elif no_of_groups == 6:
        venn(sets_dict, fontsize=font_size, legend_loc=legend_loc, fmt='{size:,}')

    else:
        venn(sets_dict, fontsize=font_size, legend_loc=legend_loc, fmt='{size:,} ({percentage:.1f}%)')

    plt.title(
        f'{pseudovenn_prefix}Venn Diagram' + (f' Grouped by {_clean_tuple(grouping_columns)}' if grouping_columns != ['FILENAME'] else ''),
        y=title_y,
        fontsize=font_size
    )

    venn_figure = plt.gcf()
    plt.close()

    if return_intersection:
        intersection_set = sets[0].intersection(*sets[1:])
        
        compare_set = data.copy(deep=True)

        intersection_df = (
            compare_set
            .drop_duplicates('KEY')
            .loc[compare_set['KEY'].isin(intersection_set)]
            .drop(columns=['FILENAME'])
            .drop(columns=['KEY'])
            .sort_values(by=['CHROM', 'POS'])
        )

        return _fig_to_png_bytes(venn_figure), intersection_df

    return _fig_to_png_bytes(venn_figure)


def _venn1(a_set: dict, fontsize: float = 8.0, legend_loc: str = 'upper right'):
    label = list(a_set.keys())[0]

    plt.rcParams['figure.figsize'] = (8, 8)

    fig, ax = plt.subplots()

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.set_aspect('equal')

    ax.add_patch(plt.Circle(
        (0, 0),
        radius=0.5,
        facecolor='#B499BA',
        edgecolor='#6E3B7B',
        label=label
    ))

    set_size = len(a_set[label])
    set_percentage = 100 if set_size > 0 else 0

    ax.text(0, 0, f'{set_size:,} ({set_percentage:.1f}%)', ha='center', va='center', fontsize=fontsize)
    ax.legend(loc=legend_loc, fontsize=fontsize)

    return fig


def _fig_to_png_bytes(fig: plt.figure) -> BytesIO:
    figure_image_bytes = BytesIO()
    fig.savefig(figure_image_bytes, format='png')
    figure_image_bytes.seek(0)
    return figure_image_bytes
