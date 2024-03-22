from dash import html

from layout import ids, styles

upload_display = (
    html.Div(id=ids.display_upload__display__div, style=styles.display_pane, children=[
        html.Div(id=ids.display_upload__compare_set_summary_card__div),
        html.Div(id=ids.display_upload__golden_set_summary_card__div),
        html.Div(id=ids.display_upload__metadata_summary_card__div),
        html.Div(id=ids.display_upload__regions_summary_card__div),
    ])
)
