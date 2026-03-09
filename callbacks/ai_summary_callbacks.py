from dash import Input, Output, callback

from ai_summary_config import AI_SUMMARY_CONFIG
from services.ai_summary_service import get_ai_summary


def _register_ai_summary_callback(page_key: str):
    @callback(
        Output(f"ai-summary-output-{page_key}", "children"),
        Input(f"ai-summary-btn-{page_key}", "n_clicks"),
        prevent_initial_call=True,
    )
    def _update_ai_summary(_n_clicks):
        return get_ai_summary(page_key)


for _page_key in AI_SUMMARY_CONFIG.keys():
    _register_ai_summary_callback(_page_key)
