import dash_mantine_components as dmc

from theme import MUTED_TEXT_COLOR


def nav_link(label: str, href: str, icon_text: str):
    link = dmc.Anchor(
        dmc.Group(
            gap="sm",
            wrap="nowrap",
            children=[
                dmc.ThemeIcon(
                    dmc.Text(icon_text, fw=700, size="xs", className="sidebar-icon-text"),
                    radius="sm",
                    variant="light",
                    className="sidebar-icon",
                ),
                dmc.Text(label, size="sm", className="sidebar-label"),
            ],
        ),
        href=href,
        underline="never",
        className="sidebar-link",
    )

    return dmc.Tooltip(
        label=label,
        position="right",
        withArrow=True,
        children=link,
    )


def sidebar_nav():
    return dmc.Stack(
        gap="lg",
        children=[
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Text(
                        "TCA",
                        size="xs",
                        fw=700,
                        c=MUTED_TEXT_COLOR,
                        tt="uppercase",
                        className="sidebar-section",
                    ),
                    nav_link("Summary", "/tca/summary", "S"),
                    nav_link("Execution", "/tca/execution", "E"),
                ],
            ),
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Text(
                        "ARX",
                        size="xs",
                        fw=700,
                        c=MUTED_TEXT_COLOR,
                        tt="uppercase",
                        className="sidebar-section",
                    ),
                    nav_link("Summary", "/arx/summary", "S"),
                    nav_link("Analysis", "/arx/analysis", "A"),
                ],
            ),
        ],
    )
