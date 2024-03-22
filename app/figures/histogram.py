import plotly.express as px

from layout import styles


def histogram(data, x, y, title='', font_size=12.0):
    fig = px.histogram(
        data,
        x=x,
        y=y,
        color_discrete_sequence=[styles.blue]
    )

    fig.update_layout(
        title_text=title,
        title_x=0.5,
        title_y=0.975,

        xaxis_title_text=x,
        yaxis_title_text=y,
        font={'size': font_size}
    )

    fig.update_traces(
        hovertemplate=f'Filename: %{{x}}<br># of Variants: %{{y}}'
    )

    return fig
