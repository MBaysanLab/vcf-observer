from concurrent.futures import ProcessPoolExecutor
from itertools import repeat

import numpy as np
import pandas as pd

from data.file_readers import read_local_bed_files


def _sort_df_by_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if pd.Index(df[column]).is_monotonic_increasing:
        return df
    else:
        return df.sort_values(by=column)


def _filter_vcf_with_bed_single_chrom(vcf_df: pd.DataFrame, bed_df: pd.DataFrame, outside_regions: bool) -> pd.DataFrame:
    mask = np.zeros(len(vcf_df), dtype=bool)

    positions = vcf_df['POS'].to_numpy() - 1  # VCF indexes are 1-based, BED indexes are 0-based
    region_starts = bed_df['START'].to_numpy()
    region_ends = bed_df['END'].to_numpy()

    current_variant_index = 0
    current_region_index = 0
    no_of_variants = len(vcf_df)
    no_of_regions = len(bed_df)
    while (current_variant_index < no_of_variants and
           current_region_index < no_of_regions):
        current_pos = positions[current_variant_index]
        current_start = region_starts[current_region_index]
        current_end = region_ends[current_region_index]

        if current_pos < current_start:
            current_variant_index += 1
            continue

        if current_start <= current_pos < current_end:
            mask[current_variant_index] = True
            current_variant_index += 1
            continue

        if current_end <= current_pos:
            current_region_index += 1
            continue

    final_mask = ~mask if outside_regions else mask

    return vcf_df[final_mask]


def filter_pass(df: pd.DataFrame, filter_options: list) -> pd.DataFrame:
    if 'filter_pass' in filter_options:
        return df[df['FILTER_PASS']]

    return df


def filter_vcf_with_bed(vcf_df: pd.DataFrame, bed_df: pd.DataFrame, outside_regions: bool) -> pd.DataFrame:
    filtered_data = []
    to_be_calculated_vcf_dfs = []
    to_be_calculated_bed_dfs = []
    region_groupings = bed_df.groupby('CHROM')

    for chrom, variants in vcf_df.groupby('CHROM'):
        if chrom in region_groupings.groups:
            current_regions = region_groupings.get_group(chrom)

            for _, variants_of_file in variants.groupby('FILENAME'):
                to_be_calculated_vcf_dfs.append(variants_of_file)
                to_be_calculated_bed_dfs.append(current_regions)
        else:
            if outside_regions:
                filtered_data.append(variants)

    with ProcessPoolExecutor() as executor:
        filtered_data += list(executor.map(
            _filter_vcf_with_bed_single_chrom,
            to_be_calculated_vcf_dfs,
            to_be_calculated_bed_dfs,
            repeat(outside_regions, len(to_be_calculated_vcf_dfs))
        ))

    if filtered_data:
        return pd.concat(filtered_data)
    else:
        return pd.DataFrame()


def filter_regions(
        vcf_df: pd.DataFrame,
        genomic_regions: str,
        inside_outside_regions: list,
        regions_data: pd.DataFrame,
) -> pd.DataFrame:
    if genomic_regions == 'none':
        return vcf_df

    outside_regions = inside_outside_regions == 'outside_regions'

    if genomic_regions in ['custom']:
        bed_df = regions_data
    else:
        bed_df = read_local_bed_files(['../BED Files/' + genomic_regions])

    return filter_vcf_with_bed(vcf_df, bed_df, outside_regions)


def filter_chromosome(vcf_df: pd.DataFrame, chromosome: str):
    if chromosome == 'any':
        return vcf_df

    return vcf_df[vcf_df['CHROM'] == chromosome]


def filter_variant_type(vcf_df: pd.DataFrame, variant_type: str):
    if variant_type == 'all':
        return vcf_df

    if variant_type == 'snp':
        return vcf_df[
            (vcf_df['REF'].apply(lambda x: len(x) == 1) &
             vcf_df['ALT'].apply(lambda x: len(x) == 1))
        ]

    if variant_type == 'indel':
        return vcf_df[
            (vcf_df['REF'].apply(lambda x: len(x) != 1) |
             vcf_df['ALT'].apply(lambda x: len(x) != 1))
        ]

    raise ValueError(f'Unexpected variant type ` {variant_type} `.')
