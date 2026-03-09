from dash import Dash, Input, Output, State, page_container
import dash_mantine_components as dmc

import callbacks.ai_summary_callbacks  # noqa: F401
from components.shell import app_shell
from services.cache import cache
from theme import THEME

app = Dash(
    __name__,
    use_pages=False,
    suppress_callback_exceptions=True,
)

cache.init_app(
    app.server,
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": "dash_cache",
        "CACHE_DEFAULT_TIMEOUT": 300,
    },
)

app.use_pages = True
app.enable_pages()

app.title = "Execution Analytics"

app.layout = dmc.MantineProvider(
    theme=THEME,
    defaultColorScheme="light",
    children=app_shell(page_container),
)

server = app.server


@app.callback(
    Output("sidebar-open", "data"),
    Output("sidebar-burger-icon", "opened"),
    Output("app-shell", "navbar"),
    Output("app-navbar", "className"),
    Input("sidebar-burger", "n_clicks"),
    State("sidebar-open", "data"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, is_open):
    new_state = not is_open

    navbar_config = {
        "width": 260 if new_state else 72,
        "breakpoint": "sm",
        "collapsed": {"desktop": False, "mobile": False},
    }

    navbar_class = "sidebar-expanded" if new_state else "sidebar-collapsed"

    return new_state, new_state, navbar_config, navbar_class


if __name__ == "__main__":
    app.run(debug=True)
