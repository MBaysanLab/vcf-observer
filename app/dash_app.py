import os

from dash import Dash
import dash_bootstrap_components as dbc

import config


if config.bundled_mode:
    app_directory = os.path.abspath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir,
        os.pardir
    ))
    assets_directory = os.path.join(app_directory, 'assets')
else:
    assets_directory = 'assets'

app = Dash(
    __name__,
    title='VCF Observer',
    update_title='VCF Observing...',
    external_stylesheets=[dbc.themes.LITERA],
    assets_folder=assets_directory
)
