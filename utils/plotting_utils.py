import plotly.graph_objects as go

from theme import CHART_MARGIN, EMPTY_FIG_BG, EMPTY_FIG_FONT


def apply_standard_chart_layout(fig):
    fig.update_layout(margin=CHART_MARGIN)
    return fig


def empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=EMPTY_FIG_FONT,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(margin=CHART_MARGIN, plot_bgcolor=EMPTY_FIG_BG)
    return fig
