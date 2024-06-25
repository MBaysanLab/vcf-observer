from dash import dcc, html

from layout import components, ids, styles
import config
from data.file_readers import read_local_files_as_b64


def test_files(directory, filenames):
    if config.auto_upload:
        return (
            filenames,
            read_local_files_as_b64(directory, filenames),
        )

    return None, None


def upload_label(label):
    return html.H6(label)


def multi_upload(id_value, preloaded_files=(None, None)):
    return (
        dcc.Upload(
            id=id_value,
            children=html.Div([
                'Upload all files together'
            ]),
            multiple=True,
            style={
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
            },
            filename=preloaded_files[0],
            contents=preloaded_files[1],
        )
    )


def upload_result(id_value):
    return html.Div(id=id_value, style=styles.file_upload_result)


upload_tab = (
    dcc.Tab(label='Upload', value='tab-upload', style=styles.tab, selected_style=styles.tab_selected, children=[
        upload_label('Compare Set'),
        multi_upload(ids.navbar_upload__compare_set__upload, preloaded_files=test_files(config.test_files_directory, config.compare_set_test_files)),
        upload_result(ids.navbar_upload__compare_set_upload_result__div),

        upload_label('Golden Set'),
        multi_upload(ids.navbar_upload__golden_set__upload, preloaded_files=test_files(config.test_files_directory, config.golden_set_test_files)),
        upload_result(ids.navbar_upload__golden_set_upload_result__div),

        upload_label('Metadata'),
        multi_upload(ids.navbar_upload__metadata__upload, preloaded_files=test_files(config.test_files_directory, config.metadata_test_files)),
        upload_result(ids.navbar_upload__metadata_upload_result__div),

        upload_label('Genomic Regions'),
        multi_upload(ids.navbar_upload__regions__upload, preloaded_files=test_files(config.test_files_directory, config.regions_test_files)),
        upload_result(ids.navbar_upload__regions_upload_result__div),

        html.Div('*Max size per file: 200 MB', style={'fontSize': '0.8em', 'fontStyle': 'italic', 'paddingTOp': '1em'}),

        dcc.Store(id=ids.navbar_upload__compare_set_valid__store, data='compare_set_is_invalid'),
        dcc.Store(id=ids.navbar_upload__golden_set_valid__store, data='golden_set_is_invalid'),
        dcc.Store(id=ids.navbar_upload__metadata_valid__store, data='metadata_is_invalid'),
        dcc.Store(id=ids.navbar_upload__regions_valid__store, data='regions_is_invalid'),

        components.button(ids.navbar_upload__go_to_analyze__button, 'Analyze >'),
    ])
)
