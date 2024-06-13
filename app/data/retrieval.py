import pandas as pd
from dash import html

import data.filtering
from callbacks.helpers import large_centered_text
from data.cache import (
    get_compare_set_cache,
    get_golden_set_cache,
    get_metadata_cache,
    get_regions_cache,
)
from data.filtering import filter_pass, filter_regions, filter_chromosome, filter_variant_type


def get_uploaded_data(
        session_id: str,
        compare_set_valid: str = None,
        golden_set_valid: str = None,
        metadata_valid: str = None,
        regions_valid: str = None,
        filter_options: list = ('filter_pass',),
        genomic_regions: str = 'none',
        inside_outside_regions: list = (),
        on_chromosome: str = 'any',
        variant_type: str = 'all',
) -> (list, list, bool):
    data = []
    notices = []
    any_invalidity = False

    regions = pd.DataFrame()
    regions_invalidity = True
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

    compare_set_filenames = None
    if compare_set_valid:
        (
            compare_set,
            compare_set_notice,
            compare_set_invalidity
        ) = get_uploaded_compare_set(
            session_id,
            compare_set_valid,
            filter_options,
            genomic_regions,
            inside_outside_regions,
            regions,
            regions_invalidity,
            on_chromosome,
            variant_type,
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
        ) = get_uploaded_golden_set(
            session_id,
            golden_set_valid,
            filter_options,
            genomic_regions,
            inside_outside_regions,
            regions,
            regions_invalidity,
            on_chromosome,
            variant_type,
        )

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

    return data, notices, any_invalidity


def get_uploaded_compare_set(
        session_id: str,
        compare_set_valid: str,
        pass_filter: list,
        genomic_regions: str,
        inside_outside_regions: list,
        regions_data: pd.DataFrame,
        regions_invalidity: bool,
        on_chromosome: str,
        variant_type: str,
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

    ordered_filtered_compare_set = None
    if not invalidity:
        pass_filtered_compare_set = filter_pass(compare_set, pass_filter)
        stringent_filtered_compare_set = filter_regions(
            pass_filtered_compare_set,
            genomic_regions,
            inside_outside_regions,
            regions_data
        ) if not regions_invalidity else pass_filtered_compare_set
        chrom_stringent_pass_filtered_compare_set = filter_chromosome(stringent_filtered_compare_set, on_chromosome)
        type_chrom_stringent_pass_filtered_compare_set = filter_variant_type(chrom_stringent_pass_filtered_compare_set, variant_type)

        if len(type_chrom_stringent_pass_filtered_compare_set) == 0:
            invalidity = True
            notice = large_centered_text('Zero variants. Try different options.')
        else:
            ordered_filtered_compare_set = type_chrom_stringent_pass_filtered_compare_set

    return ordered_filtered_compare_set, notice, invalidity


def get_uploaded_golden_set(
        session_id: str,
        valid: str,
        pass_filter: list,
        genomic_regions: str,
        inside_outside_regions: list,
        regions_data: pd.DataFrame,
        regions_invalidity: bool,
        on_chromosome: str,
        variant_type: str,
) -> (pd.DataFrame, html.H3, bool):
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

    ordered_filtered_golden_set = None
    if not invalidity:
        pass_filtered_golden_set = filter_pass(golden_set, pass_filter)
        stringent_filtered_golden_set = filter_regions(
            pass_filtered_golden_set,
            genomic_regions,
            inside_outside_regions,
            regions_data
        ) if not regions_invalidity else pass_filtered_golden_set
        chrom_stringent_pass_filtered_golden_set = filter_chromosome(stringent_filtered_golden_set, on_chromosome)
        type_chrom_stringent_pass_filtered_golden_set = filter_variant_type(chrom_stringent_pass_filtered_golden_set, variant_type)

        if len(type_chrom_stringent_pass_filtered_golden_set) == 0:
            invalidity = True
            notice = large_centered_text('Zero variants. Try different options.')
        else:
            ordered_filtered_golden_set = type_chrom_stringent_pass_filtered_golden_set

    return ordered_filtered_golden_set, notice, invalidity


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
