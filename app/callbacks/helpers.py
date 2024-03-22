from dash import html


def get_first_element(a_list):
    if len(a_list) > 0:
        return a_list[0]
    else:
        return None


def get_second_element(a_list):
    if len(a_list) > 1:
        return a_list[1]
    else:
        return get_first_element(a_list)


def normalize_upload_filename(value) -> list:
    if value is None:
        return []
    else:
        return value


def normalize_dropdown_value(value) -> list:
    if isinstance(value, list):
        return value
    elif value is None:
        return []
    else:
        return [value]


def large_centered_text(text):
    return html.H3(text, style={'paddingTop': '3em', 'textAlign': 'center', })


placeholder = large_centered_text('Your analysis results will appear here.')
