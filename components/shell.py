from dash import dcc, html
import dash_mantine_components as dmc

from components.nav import sidebar_nav


def app_shell(page_container):
    return html.Div(
        [
            dcc.Store(id="sidebar-open", data=True),
            dmc.AppShell(
                [
                    dmc.AppShellHeader(
                        dmc.Group(
                            justify="space-between",
                            h="100%",
                            px="md",
                            children=[
                                dmc.Group(
                                    gap="sm",
                                    children=[
                                        dmc.UnstyledButton(
                                            id="sidebar-burger",
                                            n_clicks=0,
                                            children=dmc.Burger(
                                                id="sidebar-burger-icon",
                                                opened=True,
                                                size="sm",
                                            ),
                                        ),
                                        dmc.ThemeIcon("EA", variant="filled", radius="xl"),
                                        dmc.Stack(
                                            gap=0,
                                            children=[
                                                dmc.Text("Execution Analytics", fw=700),
                                                dmc.Text(
                                                    "Dash + Mantine starter app",
                                                    size="xs",
                                                    c="dimmed",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dmc.Badge("DEV", variant="light"),
                            ],
                        )
                    ),
                    dmc.AppShellNavbar(
                        id="app-navbar",
                        p="md",
                        className="sidebar-expanded",
                        children=sidebar_nav(),
                    ),
                    dmc.AppShellMain(
                        dmc.Box(
                            w="100%",
                            p="md",
                            children=page_container,
                        )
                    ),
                ],
                id="app-shell",
                header={"height": 70},
                navbar={
                    "width": 260,
                    "breakpoint": "sm",
                    "collapsed": {"desktop": False, "mobile": False},
                },
                padding=0,
            ),
        ]
    )
