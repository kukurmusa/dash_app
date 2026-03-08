import dash
from dash import Input, Output, callback
import dash_mantine_components as dmc
import plotly.express as px

from components.cards import section_title, kpi_card, chart_card
from components.filters import labelled_select
from services.tca_service import get_tca_execution_data

dash.register_page(__name__, path="/tca/execution", name="TCA Execution")

df = get_tca_execution_data()

region_options = [{"label": "All", "value": "All"}] + [
    {"label": x, "value": x} for x in sorted(df["region"].unique())
]

layout = dmc.Stack(
    gap="lg",
    children=[
        section_title("TCA Execution", "Algo-level execution view"),
        dmc.Card(
            dmc.Grid(
                [
                    dmc.GridCol(
                        labelled_select(
                            "Region",
                            "tca-execution-region",
                            region_options,
                            value="All",
                        ),
                        span={"base": 12, "sm": 4},
                    ),
                ]
            )
        ),
        dmc.SimpleGrid(
            cols={"base": 1, "sm": 2, "lg": 4},
            spacing="lg",
            children=[
                kpi_card("tca-execution-kpi-orders", "Algo Orders"),
                kpi_card("tca-execution-kpi-fill", "Avg Fill Rate"),
                kpi_card("tca-execution-kpi-slip", "Avg Slippage"),
                kpi_card("tca-execution-kpi-participation", "Avg Participation"),
            ],
        ),
        dmc.Grid(
            [
                dmc.GridCol(
                    chart_card("Fill Rate by Algo", "tca-execution-fill-chart"),
                    span={"base": 12, "lg": 6},
                ),
                dmc.GridCol(
                    chart_card("Slippage by Algo", "tca-execution-slippage-chart"),
                    span={"base": 12, "lg": 6},
                ),
            ]
        ),
    ],
)


@callback(
    Output("tca-execution-kpi-orders", "children"),
    Output("tca-execution-kpi-fill", "children"),
    Output("tca-execution-kpi-slip", "children"),
    Output("tca-execution-kpi-participation", "children"),
    Output("tca-execution-fill-chart", "figure"),
    Output("tca-execution-slippage-chart", "figure"),
    Input("tca-execution-region", "value"),
)
def update_tca_execution(selected_region):
    filtered = df.copy()

    if selected_region and selected_region != "All":
        filtered = filtered[filtered["region"] == selected_region]

    total_orders = int(filtered["orders"].sum())
    avg_fill = filtered["fill_rate"].mean()
    avg_slip = filtered["slippage_bps"].mean()
    avg_participation = filtered["participation_rate"].mean()

    fig_fill = px.bar(filtered, x="algo", y="fill_rate", title=None)
    fig_fill.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    fig_slip = px.line(filtered, x="algo", y="slippage_bps", markers=True, title=None)
    fig_slip.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    return (
        f"{total_orders:,}",
        f"{avg_fill:.1f}%",
        f"{avg_slip:.1f} bps",
        f"{avg_participation:.1f}%",
        fig_fill,
        fig_slip,
    )