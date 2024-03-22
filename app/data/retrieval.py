from concurrent.futures import ProcessPoolExecutor
from itertools import repeat

import numpy as np
import pandas as pd
from dash import html

from callbacks.helpers import large_centered_text
from data.cache import (
    get_compare_set_cache,
    get_golden_set_cache,
    get_metadata_cache,
    get_regions_cache,
)
from data.file_readers import read_local_bed_files


def apply_filter_options(df: pd.DataFrame, filter_options: list) -> pd.DataFrame:
    if 'filter_pass' in filter_options:
        return df[df['FILTER_PASS']]

    return df


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


def apply_regions(
        vcf_df: pd.DataFrame,
        session_id: str,
        genomic_regions: str,
        regions_valid: str,
        inside_outside_regions: list,
) -> pd.DataFrame:
    if genomic_regions == 'none':
        return vcf_df

    outside_regions = inside_outside_regions == 'outside_regions'

    if genomic_regions in ['custom']:
        (
            (regions_data,),
            _,
            any_invalidity
        ) = get_uploaded_data(session_id, regions_valid=regions_valid)

        if any_invalidity:
            return vcf_df

        bed_df = regions_data
    else:
        bed_df = read_local_bed_files(['../BED Files/' + genomic_regions])

    return filter_vcf_with_bed(vcf_df, bed_df, outside_regions)


def get_uploaded_data(
        session_id: str,
        compare_set_valid: str = None,
        golden_set_valid: str = None,
        metadata_valid: str = None,
        regions_valid: str = None,
        filter_options: list = ('filter_pass',),
        genomic_regions: str = 'none',
        inside_outside_regions: list = (),
) -> (list, list, bool):
    data = []
    notices = []
    any_invalidity = False

    compare_set_filenames = None
    if compare_set_valid:
        (
            compare_set,
            compare_set_notice,
            compare_set_invalidity
        ) = get_uploaded_compare_set(
            session_id,
            compare_set_valid,
            regions_valid,
            filter_options,
            genomic_regions,
            inside_outside_regions,
        )

        data.append(compare_set)
        notices.append(compare_set_notice)
        any_invalidity = any_invalidity or compare_set_invalidity

        if compare_set is not None:
            compare_set_filenames = compare_set['FILENAME'].unique().tolist()

    if golden_set_valid:
        (
            golden_set,
            golden_set_notice,
            golden_set_invalidity
        ) = get_uploaded_golden_set(session_id, golden_set_valid)

        data.append(golden_set)
        notices.append(golden_set_notice)
        any_invalidity = any_invalidity or golden_set_invalidity

    if metadata_valid:
        (
            metadata,
            metadata_notice,
            metadata_invalidity
        ) = get_uploaded_metadata(session_id, metadata_valid, placeholder_filenames=compare_set_filenames)

        data.append(metadata)
        notices.append(metadata_notice)
        any_invalidity = any_invalidity or metadata_invalidity

    if regions_valid and (genomic_regions in ['custom'] or
       (compare_set_valid, golden_set_valid, metadata_valid).count(None) == 3):
        (
            regions,
            regions_notice,
            regions_invalidity
        ) = get_uploaded_regions(session_id, regions_valid)

        if (compare_set_valid, golden_set_valid, metadata_valid).count(None) == 3:
            data.append(regions)
        notices.append(regions_notice)
        any_invalidity = any_invalidity or regions_invalidity

    return data, notices, any_invalidity


def get_uploaded_compare_set(
        session_id: str,
        compare_set_valid: str,
        regions_valid: str,
        filter_options: list,
        genomic_regions: str,
        inside_outside_regions: list,
) -> (pd.DataFrame, html.H3, bool):
    compare_set = None
    notice = None
    invalidity = False

    if compare_set_valid == 'compare_set_is_valid':
        try:
            compare_set = get_compare_set_cache(session_id)
        except LookupError as e:
            invalidity = True
            notice = large_centered_text('Compare set has expired.')
    else:
        invalidity = True
        notice = large_centered_text('Compare set is invalid.')

    ordered_stringent_filtered_compare_set = None
    if not invalidity:
        filtered_compare_set = apply_filter_options(compare_set, filter_options)
        stringent_filtered_compare_set = apply_regions(
            filtered_compare_set,
            session_id,
            genomic_regions,
            regions_valid,
            inside_outside_regions
        )

        if len(stringent_filtered_compare_set) == 0:
            invalidity = True
            notice = large_centered_text('Zero variants. Try different options.')
        else:
            ordered_stringent_filtered_compare_set = stringent_filtered_compare_set

    return ordered_stringent_filtered_compare_set, notice, invalidity


def get_uploaded_golden_set(session_id: str, valid: str) -> (pd.DataFrame, html.H3, bool):
    golden_set = None
    notice = None
    invalidity = False

    if valid == 'golden_set_is_valid':
        try:
            golden_set = get_golden_set_cache(session_id)
        except LookupError as e:
            invalidity = True
            notice = large_centered_text('Golden set has expired.')
    else:
        invalidity = True
        notice = large_centered_text('Golden set is invalid.')

    return golden_set, notice, invalidity


def get_uploaded_metadata(session_id: str, valid: str, placeholder_filenames: list = None) -> (pd.DataFrame, html.H3, bool):
    metadata = None
    notice = None
    invalidity = False

    if valid == 'metadata_is_valid':
        try:
            metadata = get_metadata_cache(session_id)
        except LookupError as e:
            invalidity = True
            notice = large_centered_text('Metadata has expired.')
    else:
        invalidity = True
        notice = large_centered_text('Metadata is invalid.')

    if invalidity and placeholder_filenames:
        invalidity = False
        notice = None
        metadata = pd.DataFrame({'FILENAME': placeholder_filenames})

    return metadata, notice, invalidity


def get_uploaded_regions(session_id: str, valid: str) -> (pd.DataFrame, html.H3, bool):
    regions = None
    notice = None
    invalidity = False

    if valid == 'regions_is_valid':
        try:
            regions = get_regions_cache(session_id)
        except LookupError as e:
            invalidity = True
            notice = large_centered_text('Genomic regions have expired.')
    else:
        invalidity = True
        notice = large_centered_text('Genomic regions are invalid.')

    return regions, notice, invalidity
