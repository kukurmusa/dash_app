import dash
from dash import Input, Output, callback
import dash_mantine_components as dmc
import plotly.express as px

from components.ai_summary import ai_summary_card
from components.cards import section_title, kpi_card, chart_card
from components.filters import labelled_select
from services.tca_service import get_tca_summary_data
from utils.plotting_utils import apply_standard_chart_layout

dash.register_page(__name__, path="/tca/summary", name="TCA Summary")

df = get_tca_summary_data()

desk_options = [{"label": "All", "value": "All"}] + [
    {"label": x, "value": x} for x in sorted(df["desk"].unique())
]

layout = dmc.Stack(
    gap="lg",
    children=[
        section_title("TCA Summary", "Top-level desk and regional TCA snapshot"),
        dmc.Card(
            dmc.Grid(
                [
                    dmc.GridCol(
                        labelled_select(
                            "Desk",
                            "tca-summary-desk",
                            desk_options,
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
                kpi_card("tca-summary-kpi-orders", "Total Orders"),
                kpi_card("tca-summary-kpi-notional", "Notional"),
                kpi_card("tca-summary-kpi-fill", "Avg Fill Rate"),
                kpi_card("tca-summary-kpi-slip", "Avg Slippage"),
            ],
        ),
        dmc.Grid(
            [
                dmc.GridCol(
                    chart_card("Notional by Region", "tca-summary-notional-chart"),
                    span={"base": 12, "lg": 6},
                ),
                dmc.GridCol(
                    chart_card("Slippage by Region", "tca-summary-slippage-chart"),
                    span={"base": 12, "lg": 6},
                ),
            ]
        ),
        ai_summary_card("tca_summary"),
    ],
)


@callback(
    Output("tca-summary-kpi-orders", "children"),
    Output("tca-summary-kpi-notional", "children"),
    Output("tca-summary-kpi-fill", "children"),
    Output("tca-summary-kpi-slip", "children"),
    Output("tca-summary-notional-chart", "figure"),
    Output("tca-summary-slippage-chart", "figure"),
    Input("tca-summary-desk", "value"),
)
def update_tca_summary(selected_desk):
    filtered = df.copy()

    if selected_desk and selected_desk != "All":
        filtered = filtered[filtered["desk"] == selected_desk]

    total_orders = int(filtered["orders"].sum())
    total_notional = filtered["notional_m"].sum()
    avg_fill = filtered["fill_rate"].mean()
    avg_slip = filtered["slippage_bps"].mean()

    notional_by_region = filtered.groupby("region", as_index=False)["notional_m"].sum()
    slippage_by_region = filtered.groupby("region", as_index=False)["slippage_bps"].mean()

    fig_notional = px.bar(notional_by_region, x="region", y="notional_m", title=None)
    fig_notional = apply_standard_chart_layout(fig_notional)

    fig_slippage = px.bar(slippage_by_region, x="region", y="slippage_bps", title=None)
    fig_slippage = apply_standard_chart_layout(fig_slippage)

    return (
        f"{total_orders:,}",
        f"£{total_notional:,.0f}m",
        f"{avg_fill:.1f}%",
        f"{avg_slip:.1f} bps",
        fig_notional,
        fig_slippage,
    )
