from __future__ import annotations

from typing import Any

ARX_SUMMARY_QUERY = "arx_summary_overall"
ARX_ANALYSIS_QUERY = "arx_analysis_experiment"


def _normalize_filter_value(value: Any):
    if value in (None, "", "All"):
        return None
    return value


def build_arx_summary_query() -> dict[str, Any]:
    return {
        "query_name": ARX_SUMMARY_QUERY,
        "q": "arx.summary.overall[]",
        "params": {},
    }


def build_arx_analysis_query(
    *,
    asset_class=None,
    region=None,
    arx_status=None,
    algo=None,
    experiment_name=None,
) -> dict[str, Any]:
    params = {
        "asset_class": _normalize_filter_value(asset_class),
        "region": _normalize_filter_value(region),
        "arx_status": _normalize_filter_value(arx_status),
        "algo": _normalize_filter_value(algo),
        "experiment_name": _normalize_filter_value(experiment_name),
    }
    params = {k: v for k, v in params.items() if v is not None}

    return {
        "query_name": ARX_ANALYSIS_QUERY,
        "q": "arx.analysis.by_experiment",
        "params": params,
    }
