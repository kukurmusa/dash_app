import dash

from layouts.arx_layout import build_arx_summary_layout
import callbacks.arx_callbacks  # noqa: F401

dash.register_page(
    __name__,
    path="/arx/summary",
    name="ARX Summary",
    redirect_from=["/arx", "/arx/"],
)

layout = build_arx_summary_layout()
