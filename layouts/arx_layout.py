from dash import dash_table, html
import dash_mantine_components as dmc

from components.ai_summary import ai_summary_card
from components.cards import chart_card, kpi_card, section_title
from components.filters import labelled_select
from services.arx_service import get_arx_analysis_data
from theme import MUTED_TEXT_COLOR, PANEL_BORDER_RADIUS, TABLE_CELL_STYLE, TABLE_HEADER_STYLE, TABLE_STYLE


def _analysis_filter_options():
    df = get_arx_analysis_data()
    asset_class_options = [{"label": "All", "value": "All"}] + [
        {"label": x, "value": x} for x in sorted(df["asset_class"].unique())
    ]
    region_options = [{"label": "All", "value": "All"}] + [
        {"label": x, "value": x} for x in sorted(df["region"].unique())
    ]
    experiment_name_options = [{"label": "All", "value": "All"}] + [
        {"label": x, "value": x} for x in sorted(df["experiment_name"].unique())
    ]
    arx_status_options = [{"label": "All", "value": "All"}] + [
        {"label": x, "value": x} for x in sorted(df["arx_status"].unique())
    ]
    algo_options = [{"label": "All", "value": "All"}] + [
        {"label": x, "value": x} for x in sorted(df["algo"].unique())
    ]
    return (
        asset_class_options,
        region_options,
        arx_status_options,
        algo_options,
        experiment_name_options,
    )


def build_arx_summary_layout():
    return dmc.Stack(
        gap="lg",
        children=[
            section_title("ARX Summary", "Portfolio-wide experiment overview"),
            dmc.Card(
                dmc.Stack(
                    gap="md",
                    children=[
                        dmc.Group(
                            justify="space-between",
                            children=[
                                dmc.Title("Experiment Summary", order=4),
                                dmc.Button(
                                    "Refresh Summary",
                                    id="arx-summary-refresh",
                                    variant="filled",
                                    size="sm",
                                ),
                            ],
                        ),
                        dmc.SimpleGrid(
                            cols={"base": 1, "sm": 2, "lg": 5},
                            spacing="lg",
                            children=[
                                kpi_card("arx-summary-total-experiments", "Total Experiments", accent="blue", icon_text="E"),
                                kpi_card("arx-summary-active-experiments", "Active", accent="green", icon_text="A"),
                                kpi_card("arx-summary-completed-experiments", "Concluded", accent="gray", icon_text="C"),
                                kpi_card("arx-summary-asset-classes", "Asset Classes", accent="indigo", icon_text="AC"),
                                kpi_card("arx-summary-regions", "Regions", accent="teal", icon_text="R"),
                            ],
                        ),
                        dmc.SimpleGrid(
                            cols={"base": 1, "lg": 2},
                            spacing="lg",
                            children=[
                                dmc.Card(
                                    [
                                        dmc.Title("2 Most Recent Experiments", order=5, mb="sm"),
                                        dmc.Stack(id="arx-summary-recent-list", gap=4),
                                    ],
                                    withBorder=True,
                                ),
                                dmc.Card(
                                    [
                                        dmc.Title("2 Oldest Active Experiments", order=5, mb="sm"),
                                        dmc.Stack(id="arx-summary-oldest-active-list", gap=4),
                                    ],
                                    withBorder=True,
                                ),
                            ],
                        ),
                    ],
                )
            ),
            ai_summary_card("arx_summary"),
        ],
    )


def build_arx_analysis_layout():
    (
        asset_class_options,
        region_options,
        arx_status_options,
        algo_options,
        experiment_name_options,
    ) = _analysis_filter_options()

    return dmc.Stack(
        gap="lg",
        children=[
            section_title("ARX Analysis", "Filters, experiment breakdown, and detailed diagnostics"),
            dmc.Card(
                dmc.Grid(
                    [
                        dmc.GridCol(
                            labelled_select(
                                "Asset Class",
                                "arx-analysis-asset-class",
                                asset_class_options,
                                value="All",
                                searchable=True,
                            ),
                            span={"base": 12, "sm": 6, "lg": 2},
                        ),
                        dmc.GridCol(
                            labelled_select(
                                "Region",
                                "arx-analysis-region",
                                region_options,
                                value="All",
                                searchable=True,
                            ),
                            span={"base": 12, "sm": 6, "lg": 2},
                        ),
                        dmc.GridCol(
                            labelled_select(
                                "ARX Status",
                                "arx-analysis-status",
                                arx_status_options,
                                value="All",
                            ),
                            span={"base": 12, "sm": 6, "lg": 2},
                        ),
                        dmc.GridCol(
                            labelled_select(
                                "Algo",
                                "arx-analysis-algo",
                                algo_options,
                                value="All",
                                searchable=True,
                            ),
                            span={"base": 12, "sm": 6, "lg": 2},
                        ),
                        dmc.GridCol(
                            labelled_select(
                                "Experiment Name",
                                "arx-analysis-experiment-name",
                                experiment_name_options,
                                value="All",
                                searchable=True,
                            ),
                            span={"base": 12, "sm": 6, "lg": 2},
                        ),
                        dmc.GridCol(
                            dmc.Group(
                                justify="flex-end",
                                children=dmc.Button(
                                    "Refresh Breakdown",
                                    id="arx-analysis-refresh",
                                    variant="filled",
                                    size="sm",
                                    radius="md",
                                ),
                            ),
                            span={"base": 12, "sm": 6, "lg": 2},
                        ),
                    ]
                )
            ),
            dmc.Alert(
                "Select a specific experiment name to view the detailed breakdown.",
                id="arx-analysis-breakdown-empty",
                variant="light",
            ),
            html.Div(
                id="arx-analysis-breakdown",
                children=[
                    dmc.Card(
                        withBorder=True,
                        mb="md",
                        children=[
                            dmc.Text("Selected Experiment", size="xs", c=MUTED_TEXT_COLOR, tt="uppercase", fw=700),
                            dmc.Title("None", id="arx-analysis-selected-experiment", order=3, mt=4),
                        ],
                    ),
                    dmc.Tabs(
                        value="overview",
                        children=[
                            dmc.Paper(
                                withBorder=True,
                                p="xs",
                                radius=PANEL_BORDER_RADIUS,
                                mb="sm",
                                children=dmc.TabsList(
                                    grow=True,
                                    children=[
                                        dmc.TabsTab("Overview", value="overview"),
                                        dmc.TabsTab("Statistical Significance", value="significance"),
                                    ],
                                ),
                            ),
                            dmc.TabsPanel(
                                value="overview",
                                pt="md",
                                children=dmc.Stack(
                                    gap="lg",
                                    children=[
                                        dmc.SimpleGrid(
                                            cols={"base": 1, "sm": 2, "lg": 4},
                                            spacing="lg",
                                            children=[
                                                kpi_card("arx-analysis-kpi-orders", "Orders", accent="blue", icon_text="O"),
                                                kpi_card("arx-analysis-kpi-take", "Avg Take Rate", accent="green", icon_text="TR"),
                                                kpi_card("arx-analysis-kpi-fill", "Avg Fill Rate", accent="teal", icon_text="FR"),
                                                kpi_card("arx-analysis-kpi-markout", "Avg 5m Markout", accent="violet", icon_text="M5"),
                                            ],
                                        ),
                                                dmc.Grid(
                                            [
                                                dmc.GridCol(
                                                    chart_card("Take Rate by Algo", "arx-analysis-take-chart"),
                                                    span={"base": 12, "lg": 6},
                                                ),
                                                dmc.GridCol(
                                                    chart_card("5m Markout by Algo", "arx-analysis-markout-chart"),
                                                    span={"base": 12, "lg": 6},
                                                ),
                                            ]
                                        ),
                                        dmc.Card(
                                            [
                                                dmc.Group(
                                                    justify="space-between",
                                                    mb="md",
                                                    children=[dmc.Title("Experiment Detail Table", order=4)],
                                                ),
                                                dash_table.DataTable(
                                                    id="arx-analysis-detail-table",
                                                    columns=[
                                                        {"name": "Date", "id": "as_of"},
                                                        {"name": "Experiment", "id": "experiment_name"},
                                                        {"name": "ARX Status", "id": "arx_status"},
                                                        {"name": "Algo", "id": "algo"},
                                                        {"name": "Asset Class", "id": "asset_class"},
                                                        {"name": "Region", "id": "region"},
                                                        {"name": "Orders", "id": "orders"},
                                                        {"name": "Take Rate", "id": "take_rate"},
                                                        {"name": "Fill Rate", "id": "fill_rate"},
                                                        {"name": "5m Markout (bps)", "id": "markout_5m_bps"},
                                                    ],
                                                    data=[],
                                                    page_size=8,
                                                    style_table=TABLE_STYLE,
                                                    style_header=TABLE_HEADER_STYLE,
                                                    style_cell=TABLE_CELL_STYLE,
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ),
                            dmc.TabsPanel(
                                value="significance",
                                pt="md",
                                children=dmc.Stack(
                                    gap="lg",
                                    children=[
                                        dmc.Card(
                                            [
                                                dmc.Group(
                                                    justify="space-between",
                                                    children=[
                                                        dmc.Title("A/B Significance (vs Peer Experiments)", order=4),
                                                        dmc.Badge(id="arx-analysis-significance-badge", variant="light"),
                                                    ],
                                                ),
                                                dmc.Text(id="arx-analysis-significance-summary", mt="sm", size="sm"),
                                                dmc.Text(id="arx-analysis-significance-detail", mt="xs", size="sm", c=MUTED_TEXT_COLOR),
                                            ]
                                        ),
                                        chart_card("Fill Rate Comparison With Confidence Bands", "arx-analysis-ab-chart"),
                                    ],
                                ),
                            ),
                        ],
                    )
                ],
            ),
            ai_summary_card("arx_analysis"),
        ],
    )
