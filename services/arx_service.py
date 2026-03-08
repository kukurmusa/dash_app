import pandas as pd

from services.cache import cache
from services.kdb_service import execute_kdb_query
from utils.kdb_queries import build_arx_analysis_query, build_arx_summary_query


@cache.memoize(timeout=300)
def get_arx_summary_data() -> dict:
    query = build_arx_summary_query()
    return execute_kdb_query(query["query_name"], query["params"])


def get_arx_analysis_result(
    *,
    asset_class=None,
    region=None,
    arx_status=None,
    algo=None,
    experiment_name=None,
) -> dict:
    query = build_arx_analysis_query(
        asset_class=asset_class,
        region=region,
        arx_status=arx_status,
        algo=algo,
        experiment_name=experiment_name,
    )
    return execute_kdb_query(query["query_name"], query["params"])


@cache.memoize(timeout=300)
def get_arx_analysis_data() -> pd.DataFrame:
    result = get_arx_analysis_result()
    return pd.DataFrame(result.get("rows", []))
