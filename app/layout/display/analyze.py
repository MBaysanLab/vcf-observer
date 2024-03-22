from dash import html

from layout import ids, styles

analyze_display = (
    html.Div(id=ids.display_analyze__display__div, children=[
        html.Div(id=ids.display_analyze__venn_display__div, style=styles.display_pane),
        html.Div(id=ids.display_analyze__clustergram_display__div, style=styles.clustergram_display_pane),
        html.Div(id=ids.display_analyze__prerec_display__div, style=styles.display_pane),
        html.Div(id=ids.display_analyze__summary_display__div, children=[
            html.Div(id=ids.display_analyze__filename_summary_display__div, style=styles.display_pane),
            html.Div(id=ids.display_analyze__metadata_summary_display__div, style=styles.display_pane),
            html.Div(id=ids.display_analyze__raw_summary_display__div, style=styles.display_pane)
        ]),
    ])
)
