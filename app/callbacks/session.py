import uuid

from dash.dependencies import Input, Output, State

from dash_app import app
from layout import ids


@app.callback(
    Output(ids.navbar_navbar__session_id__store, 'data'),
    Input(ids.navbar_navbar__session_id__store, 'storage_type'),
)
def set_session_id(_):
    return str(uuid.uuid4())
