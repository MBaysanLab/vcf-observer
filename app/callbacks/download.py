from base64 import b64decode
from io import BytesIO
from gzip import GzipFile

from dash import dcc
from dash.dependencies import Input, Output, State

from dash_app import app
from layout import ids
from data import cache
from figures.tables import df_to_csv, variant_df_to_vcf


@app.callback(
    Output(ids.navbar_analyze_venn__figure_download__download, 'data'),
    Input(ids.navbar_analyze_venn__figure_download__button, 'n_clicks'),
    Input(ids.navbar_navbar__session_id__store, 'data'),
    prevent_initial_call=True
)
def download_venn_figure(n_clicks, session_id):
    if n_clicks:
        image_data = cache.get_venn_figure_download_cache(session_id)
        return dcc.send_bytes(b64decode(image_data), 'venn.png')


@app.callback(
    Output(ids.navbar_analyze_venn__sites_download__download, 'data'),
    Input(ids.navbar_analyze_venn__sites_download__button, 'n_clicks'),
    Input(ids.navbar_navbar__session_id__store, 'data'),
    prevent_initial_call=True
)
def download_venn_sites(n_clicks, session_id):
    if n_clicks:
        intersection_sites = cache.get_venn_sites_download_cache(session_id)
        vcf = variant_df_to_vcf(intersection_sites)

        vcf_gz = BytesIO()
        GzipFile(fileobj=vcf_gz, mode='w').write(vcf.encode('utf-8'))

        return dcc.send_bytes(vcf_gz.getvalue(), 'intersection.vcf.gz')


@app.callback(
    Output(ids.navbar_analyze_summary__filename_download__download, 'data'),
    Input(ids.navbar_analyze_summary__filename_download__button, 'n_clicks'),
    Input(ids.navbar_navbar__session_id__store, 'data'),
    prevent_initial_call=True
)
def download_filename_summary(n_clicks, session_id):
    if n_clicks:
        data = cache.get_filename_download_cache(session_id)
        return dcc.send_string(df_to_csv(data), 'summary.csv')


@app.callback(
    Output(ids.navbar_analyze_summary__metadata_download__download, 'data'),
    Input(ids.navbar_analyze_summary__metadata_download__button, 'n_clicks'),
    Input(ids.navbar_navbar__session_id__store, 'data'),
    prevent_initial_call=True
)
def download_metadata_summary(n_clicks, session_id):
    if n_clicks:
        data = cache.get_metadata_download_cache(session_id)
        return dcc.send_string(df_to_csv(data), 'summary.csv')


@app.callback(
    Output(ids.navbar_analyze_summary__raw_download__download, 'data'),
    Input(ids.navbar_analyze_summary__raw_download__button, 'n_clicks'),
    Input(ids.navbar_navbar__session_id__store, 'data'),
    prevent_initial_call=True
)
def download_raw_summary(n_clicks, session_id):
    if n_clicks:
        data = cache.get_raw_download_cache(session_id)
        return dcc.send_string(df_to_csv(data), 'summary.csv')
