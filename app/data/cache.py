from data.file_readers import read_b64_vcf_files, read_b64_csv_files, read_b64_bed_files

import pandas as pd
from flask_caching import Cache

from dash_app import app

CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': './__pycache__',
    'CACHE_DEFAULT_TIMEOUT': 24*60*60,
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)


def set_compare_set_cache_as_df(session_id: str, filenames: list, file_contents: list) -> pd.DataFrame:
    cache_key = _get_compare_set_cache_key(session_id)

    data = read_b64_vcf_files(filenames, file_contents)
    cache.set(cache_key, data)

    return data


def get_compare_set_cache(session_id) -> pd.DataFrame:
    cache_key = _get_compare_set_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def set_golden_set_cache_as_df(session_id: str, filenames: list, file_contents: list) -> pd.DataFrame:
    cache_key = _get_golden_set_cache_key(session_id)

    data = read_b64_vcf_files(filenames, file_contents)
    cache.set(cache_key, data)

    return data


def get_golden_set_cache(session_id) -> pd.DataFrame:
    cache_key = _get_golden_set_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def set_metadata_cache_as_df(session_id: str, filenames: list, file_contents: list, files_needed_in_metadata: list) -> pd.DataFrame:
    cache_key = _get_metadata_cache_key(session_id)

    data = read_b64_csv_files(filenames, file_contents)
    relevant_data = data[data['FILENAME'].isin(files_needed_in_metadata)]
    cache.set(cache_key, relevant_data)

    return relevant_data


def get_metadata_cache(session_id) -> pd.DataFrame:
    cache_key = _get_metadata_cache_key(session_id)

    relevant_data = cache.get(cache_key)
    if relevant_data is None:
        raise LookupError('The cached data has timed out.')

    return relevant_data


def set_regions_cache_as_df(session_id: str, filenames: list, file_contents: list) -> pd.DataFrame:
    cache_key = _get_regions_cache_key(session_id)

    data = (read_b64_bed_files(filenames, file_contents)
            .sort_values(by=['START', 'END'])
            .reset_index(drop=True))
    cache.set(cache_key, data)

    return data


def get_regions_cache(session_id) -> pd.DataFrame:
    cache_key = _get_regions_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def set_filename_download_cache(session_id: str, data: pd.DataFrame):
    cache_key = _get_filename_download_cache_key(session_id)
    cache.set(cache_key, data)
    return


def get_filename_download_cache(session_id) -> pd.DataFrame:
    cache_key = _get_filename_download_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def set_metadata_download_cache(session_id: str, data: pd.DataFrame):
    cache_key = _get_metadata_download_cache_key(session_id)
    cache.set(cache_key, data)
    return


def get_metadata_download_cache(session_id) -> pd.DataFrame:
    cache_key = _get_metadata_download_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def set_raw_download_cache(session_id: str, data: pd.DataFrame):
    cache_key = _get_raw_download_cache_key(session_id)
    cache.set(cache_key, data)
    return


def get_raw_download_cache(session_id) -> pd.DataFrame:
    cache_key = _get_raw_download_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def set_venn_figure_download_cache(session_id: str, figure_data: str):
    cache_key = _get_venn_figure_download_cache_key(session_id)
    cache.set(cache_key, figure_data)
    return


def get_venn_figure_download_cache(session_id) -> str:
    cache_key = _get_venn_figure_download_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def set_venn_sites_download_cache(session_id: str, data: pd.DataFrame):
    cache_key = _get_venn_sites_download_cache_key(session_id)
    cache.set(cache_key, data)
    return


def get_venn_sites_download_cache(session_id) -> pd.DataFrame:
    cache_key = _get_venn_sites_download_cache_key(session_id)

    data = cache.get(cache_key)
    if data is None:
        raise LookupError('The cached data has timed out.')

    return data


def _get_compare_set_cache_key(session_id: str):
    return session_id + '_compare_set'


def _get_golden_set_cache_key(session_id: str):
    return session_id + '_golden_set'


def _get_metadata_cache_key(session_id: str):
    return session_id + '_metadata'


def _get_regions_cache_key(session_id: str):
    return session_id + '_regions'


def _get_filename_download_cache_key(session_id: str):
    return session_id + '_filename_download'


def _get_metadata_download_cache_key(session_id: str):
    return session_id + '_metadata_download'


def _get_raw_download_cache_key(session_id: str):
    return session_id + '_raw_download'


def _get_venn_figure_download_cache_key(session_id: str):
    return session_id + '_venn_figure_download'


def _get_venn_sites_download_cache_key(session_id: str):
    return session_id + '_venn_sites_download'
