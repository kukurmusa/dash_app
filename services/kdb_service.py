from __future__ import annotations

from typing import Any

import pandas as pd

from utils.kdb_queries import ARX_ANALYSIS_QUERY, ARX_SUMMARY_QUERY

_ARX_ANALYSIS_ROWS = [
    {
        "experiment_name": "Baseline",
        "asset_class": "Equities",
        "region": "UK",
        "arx_status": "Concluded",
        "algo": "VWAP",
        "as_of": "2024-01-05",
        "take_rate": 61.2,
        "fill_rate": 78.5,
        "markout_5m_bps": -1.8,
        "orders": 4200,
    },
    {
        "experiment_name": "Latency Cut",
        "asset_class": "Equities",
        "region": "EU",
        "arx_status": "Active",
        "algo": "POV",
        "as_of": "2024-01-12",
        "take_rate": 64.8,
        "fill_rate": 80.9,
        "markout_5m_bps": -1.2,
        "orders": 3980,
    },
    {
        "experiment_name": "Quote Edge",
        "asset_class": "Equities",
        "region": "US",
        "arx_status": "Active",
        "algo": "Arrival",
        "as_of": "2024-01-19",
        "take_rate": 66.1,
        "fill_rate": 81.6,
        "markout_5m_bps": -0.9,
        "orders": 4050,
    },
    {
        "experiment_name": "Baseline",
        "asset_class": "FX",
        "region": "UK",
        "arx_status": "Concluded",
        "algo": "TWAP",
        "as_of": "2024-02-02",
        "take_rate": 59.7,
        "fill_rate": 76.8,
        "markout_5m_bps": -2.1,
        "orders": 3600,
    },
    {
        "experiment_name": "Latency Cut",
        "asset_class": "FX",
        "region": "EU",
        "arx_status": "Active",
        "algo": "POV",
        "as_of": "2024-02-09",
        "take_rate": 63.4,
        "fill_rate": 79.5,
        "markout_5m_bps": -1.4,
        "orders": 3820,
    },
    {
        "experiment_name": "Quote Edge",
        "asset_class": "FX",
        "region": "US",
        "arx_status": "Concluded",
        "algo": "Arrival",
        "as_of": "2024-02-16",
        "take_rate": 65.2,
        "fill_rate": 80.3,
        "markout_5m_bps": -1.0,
        "orders": 3950,
    },
    {
        "experiment_name": "Spread Shield",
        "asset_class": "Equities",
        "region": "UK",
        "arx_status": "Active",
        "algo": "Dark Sweep",
        "as_of": "2024-02-23",
        "take_rate": 67.3,
        "fill_rate": 82.1,
        "markout_5m_bps": -0.8,
        "orders": 4100,
    },
    {
        "experiment_name": "Spread Shield",
        "asset_class": "FX",
        "region": "EU",
        "arx_status": "Concluded",
        "algo": "Dark Sweep",
        "as_of": "2024-03-01",
        "take_rate": 62.6,
        "fill_rate": 78.9,
        "markout_5m_bps": -1.3,
        "orders": 3725,
    },
]


def _filtered_analysis_rows(params: dict[str, Any]) -> list[dict[str, Any]]:
    rows = _ARX_ANALYSIS_ROWS

    for field in ("asset_class", "region", "arx_status", "algo", "experiment_name"):
        value = params.get(field)
        if value:
            rows = [row for row in rows if row[field] == value]

    return rows


def _build_summary_result() -> dict[str, Any]:
    data = pd.DataFrame(_ARX_ANALYSIS_ROWS)
    data["as_of"] = pd.to_datetime(data["as_of"])

    latest_idx = data.sort_values("as_of").groupby("experiment_name")["as_of"].idxmax()
    experiment_latest = data.loc[latest_idx, ["experiment_name", "arx_status", "as_of"]]

    oldest_active = (
        data[data["arx_status"] == "Active"]
        .groupby("experiment_name", as_index=False)
        .agg(first_as_of=("as_of", "min"))
        .sort_values("first_as_of", ascending=True)
        .head(2)
    )

    return {
        "totals": {
            "total_experiments": int(experiment_latest["experiment_name"].nunique()),
            "active_experiments": int((experiment_latest["arx_status"] == "Active").sum()),
            "concluded_experiments": int((experiment_latest["arx_status"] == "Concluded").sum()),
            "asset_classes": int(data["asset_class"].nunique()),
            "regions": int(data["region"].nunique()),
        },
        "recent_experiments": [
            {
                "experiment_name": row["experiment_name"],
                "as_of": row["as_of"].strftime("%Y-%m-%d"),
            }
            for _, row in experiment_latest.sort_values("as_of", ascending=False).head(2).iterrows()
        ],
        "oldest_active_experiments": [
            {
                "experiment_name": row["experiment_name"],
                "as_of": row["first_as_of"].strftime("%Y-%m-%d"),
            }
            for _, row in oldest_active.iterrows()
        ],
    }


def _build_analysis_result(params: dict[str, Any]) -> dict[str, Any]:
    rows = _filtered_analysis_rows(params)
    frame = pd.DataFrame(rows)

    if frame.empty:
        totals = {"orders": 0, "avg_take_rate": 0.0, "avg_fill_rate": 0.0, "avg_markout_5m_bps": 0.0}
    else:
        totals = {
            "orders": int(frame["orders"].sum()),
            "avg_take_rate": float(frame["take_rate"].mean()),
            "avg_fill_rate": float(frame["fill_rate"].mean()),
            "avg_markout_5m_bps": float(frame["markout_5m_bps"].mean()),
        }

    return {"filters_applied": params, "rows": rows, "totals": totals}


def execute_kdb_query(query_name: str, params: dict[str, Any] | None = None, *, use_mock: bool = True) -> dict[str, Any]:
    query_params = params or {}

    if not use_mock:
        raise NotImplementedError("Live kdb execution is not wired yet.")

    if query_name == ARX_SUMMARY_QUERY:
        return _build_summary_result()
    if query_name == ARX_ANALYSIS_QUERY:
        return _build_analysis_result(query_params)

    raise ValueError(f"Unsupported kdb query: {query_name}")
