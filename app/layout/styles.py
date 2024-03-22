light_gray = '#fbfbfb'
dark_gray = '#f2f2f2'
blue = '#1d7ea8'

button = {
    'backgroundColor': dark_gray,
    'height': '40px',
    'lineHeight': '30px',
    'borderWidth': '0',
    'borderRadius': '0.2em',
    'textAlign': 'center',
    'marginTop': '1em',
    'marginBottom': '1em',
    'paddingLeft': '1em',
    'paddingRight': '1em',
    'float': 'right',
    'clear': 'both',
}
download_button = {**button, 'marginRight': '1em'}
download_button.pop('float')
download_button_secondary = download_button.copy()
download_button_secondary.pop('marginTop')
tab = {
    'padding': '2px',
    'paddingTop': '6px',
    'paddingBottom': '6px',
    'background': dark_gray,
    'borderColor': dark_gray,
    'borderTopColor': dark_gray,
    'borderLeftColor': light_gray,
    'borderRightColor': light_gray,
}
tab_selected = {
    'padding': '2px',
    'paddingTop': '6px',
    'paddingBottom': '6px',
    'background': light_gray,
    'borderColor': dark_gray,
    'borderLeftColor': light_gray,
    'borderRightColor': light_gray,
    'borderTopColor': blue,
}
file_upload_result = {
    'width': '100%',
    'block-size': 'fit-content',
    'paddingLeft': '1em',
    'paddingRight': '1em',
    'paddingBottom': '1em',
    'fontSize': '0.9em',
}
demo_image = {
    'width': '30%',
    'alignSelf': 'center',
}
display_pane = {
    'block-size': 'fit-content',
    'padding': '1em',
    'background': '#ffffff',
    'minHeight': '100vh',
}
clustergram_display_pane = {**display_pane, 'background': '#f7f7f7'}
upload_summary_card = {
    'background': light_gray,
    'borderRadius': '1em',
    'paddingLeft': '1.2em',
    'paddingRight': '1.2em',
    'paddingTop': '0.9em',
    'paddingBottom': '0.3em',
    'marginTop': '1em',
}
checklist = {
    'accent-color': blue,
    'marginLeft': '10px',
    'marginBottom': '0.8em',
}
radio_items = {
    'accent-color': blue,
    'marginLeft': '10px',
    'paddingBottom': '1em',
}
dropdown = {
    'marginTop': '0.4em',
    'marginBottom': '0.8em'
}
dropdown_with_related_element_below = {**dropdown, 'marginBottom': '0.4em'}
