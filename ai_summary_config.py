AI_SUMMARY_CONFIG = {
    "tca_summary": {
        "system_prompt": (
            "You are an execution analytics assistant. Summarize key performance insights in plain business language."
        ),
        "user_prompt": (
            "Summarize this TCA Summary page content in 3-5 concise bullet points.\n\n"
            "Page content:\n{page_content}"
        ),
        "page_content": (
            "TCA Summary page with desk filter, KPIs (orders, notional, fill rate, slippage), "
            "and charts for notional/slippage by region."
        ),
        "dummy_summary": (
            "TCA Summary (dummy): Overall orders and notional are concentrated in two regions. "
            "Fill rate is stable while slippage remains within expected range."
        ),
    },
    "tca_execution": {
        "system_prompt": (
            "You are an execution analytics assistant. Summarize algo-level execution behavior and outliers."
        ),
        "user_prompt": (
            "Summarize this TCA Execution page content in 3-5 concise bullet points.\n\n"
            "Page content:\n{page_content}"
        ),
        "page_content": (
            "TCA Execution page with region filter, KPIs (orders, fill rate, slippage, participation), "
            "and charts for fill/slippage by algo."
        ),
        "dummy_summary": (
            "TCA Execution (dummy): Algo performance is mixed by region, with one algo showing stronger fill "
            "at the cost of slightly higher participation."
        ),
    },
    "arx_summary": {
        "system_prompt": (
            "You are an ARX experiment analyst. Summarize portfolio-level experiment activity and lifecycle state."
        ),
        "user_prompt": (
            "Summarize this ARX Summary page content in 3-5 concise bullet points.\n\n"
            "Page content:\n{page_content}"
        ),
        "page_content": (
            "ARX Summary page with total/active/concluded experiments, asset classes, regions, "
            "and recent vs oldest active experiment lists."
        ),
        "dummy_summary": (
            "ARX Summary (dummy): Active experiments outnumber concluded ones, with broad coverage across "
            "asset classes and regions. Recent launches indicate continued testing cadence."
        ),
    },
    "arx_analysis": {
        "system_prompt": (
            "You are an ARX experiment analyst. Summarize experiment diagnostics, KPI trends, and significance context."
        ),
        "user_prompt": (
            "Summarize this ARX Analysis page content in 3-5 concise bullet points.\n\n"
            "Page content:\n{page_content}"
        ),
        "page_content": (
            "ARX Analysis page with filters (asset class, region, status, algo, experiment), KPI cards, "
            "breakdown charts, detail table, and statistical significance tab."
        ),
        "dummy_summary": (
            "ARX Analysis (dummy): Selected experiment shows KPI deltas versus peers with moderate markout "
            "improvement. Statistical signal is directional but should be validated with larger sample size."
        ),
    },
}
