from dash import dcc, html

from layout import styles


def button(id_value, text):
    return html.Button(text, id=id_value, style=styles.button, className='button')


def download_button(id_value, text):
    return html.Button(text, id=id_value, style=styles.download_button, className='button')


def download_button_secondary(id_value, text):
    return html.Button(text, id=id_value, style=styles.download_button_secondary, className='button')


def dropdown_label(label):
    return html.H6(label)


def multi_dropdown(id_value, style=styles.dropdown):
    return dcc.Dropdown(id=id_value, className='multi-dropdown', style=style, multi=True)


def grouping_method_dropdown(id_value, style=styles.dropdown):
    return (
        dcc.Dropdown(id=id_value, style=style, clearable=False, value='union', options={
            'union': '(Union)',
            'inter': '(Intersection)',
            'major': '(Majority)',
        })
    )


def font_size_selector(id_value, default_value=12, div_id=''):
    return (html.Div(
        id=div_id,
        style={
            'marginTop': '1em',
            'height': 'fit-contents',
        },
        children=[
            html.H6('Font Size:', style={'display': 'inline-block', 'marginTop': '6px'}),
            dcc.Input(
                id=id_value,
                type='number',
                placeholder=default_value,
                value=default_value,
                style={
                    'maxWidth': '5em',
                    'marginLeft': '1em',
                    'paddingBottom': '3px',
                    'float': 'right',
                    'borderStyle': 'solid',
                    'borderWidth': 'thin',
                    'borderRadius': '4px',
                    'borderColor':  '#cccccc',
                },
                min=5,
                max=50,
            )
        ],
    ))
