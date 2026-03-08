from dash import dcc
import dash_mantine_components as dmc


def section_title(title: str, subtitle: str | None = None):
    children = [dmc.Title(title, order=2)]
    if subtitle:
        children.append(dmc.Text(subtitle, c="dimmed", size="sm"))
    return dmc.Stack(gap=2, children=children)


def kpi_card(component_id: str, title: str, accent: str = "blue", icon_text: str | None = None):
    header_children = []
    if icon_text:
        header_children.append(
            dmc.ThemeIcon(
                icon_text,
                size="sm",
                radius="xl",
                variant="light",
                color=accent,
            )
        )
    header_children.append(dmc.Text(title, size="sm", fw=600, c="dimmed"))

    return dmc.Card(
        [
            dmc.Group(gap="xs", children=header_children),
            dmc.Title(id=component_id, order=2, children="--"),
        ],
        style={"borderTop": f"3px solid var(--mantine-color-{accent}-6)"},
    )


def chart_card(title: str, graph_id: str):
    return dmc.Card(
        [
            dmc.Group(
                justify="space-between",
                mb="md",
                children=[dmc.Title(title, order=4)],
            ),
            dcc.Graph(
                id=graph_id,
                config={"displayModeBar": False},
                style={"height": "360px"},
            ),
        ]
    )
