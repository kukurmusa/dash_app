import dash

from layouts.arx_layout import build_arx_analysis_layout
import callbacks.arx_callbacks  # noqa: F401

dash.register_page(
    __name__,
    path="/arx/analysis",
    name="ARX Analysis",
)

layout = build_arx_analysis_layout()
