import math

from dash import Input, Output, State, callback
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from services.arx_service import get_arx_analysis_result, get_arx_summary_data


def _list_items_from_rows(rows: pd.DataFrame, date_col: str) -> list:
    if rows.empty:
        return [dmc.Text("No experiments available", size="sm", c="dimmed")]

    return [
        dmc.Group(
            justify="space-between",
            children=[
                dmc.Text(str(row["experiment_name"]), fw=500, size="sm"),
                dmc.Text(pd.to_datetime(row[date_col]).strftime("%Y-%m-%d"), size="xs", c="dimmed"),
            ],
        )
        for _, row in rows.iterrows()
    ]


def _empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 14, "color": "#6b7280"},
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor="white")
    return fig


def _format_table(df_table: pd.DataFrame) -> list:
    if df_table.empty:
        return []

    view = df_table.copy()
    view["as_of"] = pd.to_datetime(view["as_of"]).dt.strftime("%Y-%m-%d")
    view["orders"] = view["orders"].astype(int)
    view["take_rate"] = view["take_rate"].round(2)
    view["fill_rate"] = view["fill_rate"].round(2)
    view["markout_5m_bps"] = view["markout_5m_bps"].round(2)

    return view[
        [
            "as_of",
            "experiment_name",
            "arx_status",
            "algo",
            "asset_class",
            "region",
            "orders",
            "take_rate",
            "fill_rate",
            "markout_5m_bps",
        ]
    ].to_dict("records")


def _ab_significance_approx(filtered_full: pd.DataFrame, selected_experiment_name: str):
    treatment = filtered_full[filtered_full["experiment_name"] == selected_experiment_name]
    peers = filtered_full[filtered_full["experiment_name"] != selected_experiment_name]

    if treatment.empty or peers.empty:
        return (
            "Insufficient data",
            "Need selected experiment and peer experiment rows after filters.",
            "No significance test run.",
            "gray",
            _empty_figure("Not enough rows for A/B significance"),
        )

    metric = "fill_rate"
    t_values = treatment[metric].astype(float)
    c_values = peers[metric].astype(float)

    if len(t_values) < 2 or len(c_values) < 2:
        return (
            "Insufficient data",
            "At least 2 observations per cohort are required.",
            "No significance test run.",
            "gray",
            _empty_figure("Need >=2 observations in each cohort"),
        )

    t_mean = float(t_values.mean())
    c_mean = float(c_values.mean())
    t_std = float(t_values.std(ddof=1))
    c_std = float(c_values.std(ddof=1))
    t_n = len(t_values)
    c_n = len(c_values)

    se = math.sqrt((t_std ** 2 / t_n) + (c_std ** 2 / c_n))
    if se == 0:
        return (
            "No variability",
            "Cannot compute significance because standard error is zero.",
            "No significance test run.",
            "yellow",
            _empty_figure("Standard error is zero"),
        )

    z_score = (t_mean - c_mean) / se
    p_value = math.erfc(abs(z_score) / math.sqrt(2))
    significant = p_value < 0.05
    direction = "higher" if (t_mean - c_mean) >= 0 else "lower"

    summary = (
        f"{selected_experiment_name} has {abs(t_mean - c_mean):.2f} pp {direction} fill rate vs peers "
        f"(p={p_value:.4f}, z={z_score:.2f})."
    )
    detail = (
        f"Selected mean={t_mean:.2f}% (n={t_n}), Peer mean={c_mean:.2f}% (n={c_n}). "
        f"Normal approximation used for significance."
    )
    badge_color = "green" if significant else "orange"
    badge_text = "Statistically Significant" if significant else "Not Significant"

    cohorts = pd.DataFrame(
        {
            "cohort": ["Peers", selected_experiment_name],
            "mean_fill_rate": [c_mean, t_mean],
            "ci95": [1.96 * c_std / math.sqrt(c_n), 1.96 * t_std / math.sqrt(t_n)],
        }
    )
    fig = px.bar(cohorts, x="cohort", y="mean_fill_rate", title=None, color="cohort")
    fig.update_traces(error_y=dict(type="data", array=cohorts["ci95"]), texttemplate="%{y:.2f}%")
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), yaxis_title="Fill Rate (%)")

    return badge_text, summary, detail, badge_color, fig


@callback(
    Output("arx-analysis-experiment-name", "options"),
    Output("arx-analysis-experiment-name", "value"),
    Input("arx-analysis-asset-class", "value"),
    Input("arx-analysis-region", "value"),
    Input("arx-analysis-status", "value"),
    State("arx-analysis-experiment-name", "value"),
)
def update_arx_experiment_options(selected_asset_class, selected_region, selected_status, current_experiment):
    result = get_arx_analysis_result(
        asset_class=selected_asset_class,
        region=selected_region,
        arx_status=selected_status,
    )
    filtered = pd.DataFrame(result.get("rows", []))

    experiment_options = [{"label": "All", "value": "All"}]
    if not filtered.empty:
        experiment_options.extend(
            [{"label": x, "value": x} for x in sorted(filtered["experiment_name"].unique())]
        )

    valid_values = {option["value"] for option in experiment_options}
    next_value = current_experiment if current_experiment in valid_values else "All"

    return experiment_options, next_value


@callback(
    Output("arx-summary-total-experiments", "children"),
    Output("arx-summary-active-experiments", "children"),
    Output("arx-summary-completed-experiments", "children"),
    Output("arx-summary-asset-classes", "children"),
    Output("arx-summary-regions", "children"),
    Output("arx-summary-recent-list", "children"),
    Output("arx-summary-oldest-active-list", "children"),
    Input("arx-summary-refresh", "n_clicks"),
)
def update_arx_summary(_n_clicks):
    summary_result = get_arx_summary_data()
    totals = summary_result.get("totals", {})
    recent_rows = pd.DataFrame(summary_result.get("recent_experiments", []))
    oldest_active = pd.DataFrame(summary_result.get("oldest_active_experiments", []))

    if "as_of" in recent_rows.columns:
        recent_rows["as_of"] = pd.to_datetime(recent_rows["as_of"])
    if "as_of" in oldest_active.columns:
        oldest_active["as_of"] = pd.to_datetime(oldest_active["as_of"])

    return (
        f"{int(totals.get('total_experiments', 0)):,}",
        f"{int(totals.get('active_experiments', 0)):,}",
        f"{int(totals.get('concluded_experiments', totals.get('completed_experiments', 0))):,}",
        f"{int(totals.get('asset_classes', 0)):,}",
        f"{int(totals.get('regions', 0)):,}",
        _list_items_from_rows(recent_rows, "as_of"),
        _list_items_from_rows(oldest_active, "as_of"),
    )

@callback(
    Output("arx-analysis-kpi-orders", "children"),
    Output("arx-analysis-kpi-take", "children"),
    Output("arx-analysis-kpi-fill", "children"),
    Output("arx-analysis-kpi-markout", "children"),
    Output("arx-analysis-take-chart", "figure"),
    Output("arx-analysis-markout-chart", "figure"),
    Output("arx-analysis-breakdown", "style"),
    Output("arx-analysis-breakdown-empty", "style"),
    Output("arx-analysis-selected-experiment", "children"),
    Output("arx-analysis-detail-table", "data"),
    Output("arx-analysis-significance-badge", "children"),
    Output("arx-analysis-significance-badge", "color"),
    Output("arx-analysis-significance-summary", "children"),
    Output("arx-analysis-significance-detail", "children"),
    Output("arx-analysis-ab-chart", "figure"),
    Input("arx-analysis-refresh", "n_clicks"),
    State("arx-analysis-asset-class", "value"),
    State("arx-analysis-region", "value"),
    State("arx-analysis-status", "value"),
    State("arx-analysis-algo", "value"),
    State("arx-analysis-experiment-name", "value"),
)
def update_arx_analysis(
    _n_clicks,
    selected_asset_class,
    selected_region,
    selected_status,
    selected_algo,
    selected_experiment_name,
):
    analysis_result = get_arx_analysis_result(
        asset_class=selected_asset_class,
        region=selected_region,
        arx_status=selected_status,
        algo=selected_algo,
    )
    filtered_full = pd.DataFrame(analysis_result.get("rows", []))

    filtered = filtered_full.copy()

    if not selected_experiment_name or selected_experiment_name == "All":
        empty = _empty_figure("Select a specific experiment to see breakdown charts")
        return (
            "--",
            "--",
            "--",
            "--",
            empty,
            empty,
            {"display": "none"},
            {"display": "block"},
            "None",
            [],
            "Awaiting Selection",
            "gray",
            "Choose a specific experiment and click Refresh Breakdown to run A/B significance vs peers.",
            "",
            empty,
        )

    filtered = filtered[filtered["experiment_name"] == selected_experiment_name]

    if filtered.empty:
        total_orders = 0
        avg_take = 0.0
        avg_fill = 0.0
        avg_markout = 0.0
    else:
        total_orders = int(filtered["orders"].sum())
        avg_take = filtered["take_rate"].mean()
        avg_fill = filtered["fill_rate"].mean()
        avg_markout = filtered["markout_5m_bps"].mean()

    fig_take = px.bar(filtered, x="algo", y="take_rate", title=None)
    fig_take.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    fig_markout = px.bar(filtered, x="algo", y="markout_5m_bps", title=None)
    fig_markout.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    table_data = _format_table(filtered.sort_values("as_of", ascending=False))
    badge_text, sig_summary, sig_detail, badge_color, ab_fig = _ab_significance_approx(
        filtered_full,
        selected_experiment_name,
    )

    return (
        f"{total_orders:,}",
        f"{avg_take:.1f}%",
        f"{avg_fill:.1f}%",
        f"{avg_markout:.1f} bps",
        fig_take,
        fig_markout,
        {"display": "block"},
        {"display": "none"},
        selected_experiment_name,
        table_data,
        badge_text,
        badge_color,
        sig_summary,
        sig_detail,
        ab_fig,
    )
