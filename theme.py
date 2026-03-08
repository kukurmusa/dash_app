PRIMARY_COLOR = "blue"
MUTED_TEXT_COLOR = "dimmed"
DEFAULT_RADIUS = "md"
CARD_RADIUS = "lg"
ICON_RADIUS = "xl"
CHART_MARGIN = {"l": 20, "r": 20, "t": 20, "b": 20}
CHART_HEIGHT = "360px"
EMPTY_FIG_FONT = {"size": 14, "color": "#6b7280"}
EMPTY_FIG_BG = "white"
TABLE_STYLE = {"overflowX": "auto"}
TABLE_HEADER_STYLE = {"fontWeight": "700"}
TABLE_CELL_STYLE = {"textAlign": "left", "padding": "8px"}
PANEL_BORDER_RADIUS = "md"

THEME = {
    "primaryColor": PRIMARY_COLOR,
    "fontFamily": "Inter, Arial, sans-serif",
    "defaultRadius": DEFAULT_RADIUS,
    "components": {
        "Card": {
            "defaultProps": {
                "withBorder": True,
                "shadow": "sm",
                "padding": "lg",
                "radius": CARD_RADIUS,
            }
        },
        "Button": {
            "defaultProps": {
                "radius": DEFAULT_RADIUS,
                "color": PRIMARY_COLOR,
            }
        },
        "Select": {
            "defaultProps": {
                "searchable": True,
                "clearable": False,
                "size": "sm",
            }
        },
        "Title": {
            "defaultProps": {
                "order": 3,
            }
        },
        "Tabs": {
            "defaultProps": {
                "color": PRIMARY_COLOR,
                "variant": "pills",
            }
        },
    },
}
