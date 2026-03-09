import dash_mantine_components as dmc


def ai_summary_card(page_key: str):
    return dmc.Card(
        [
            dmc.Group(
                justify="space-between",
                children=[
                    dmc.Title("AI Summary", order=4),
                    dmc.Button(
                        "Get AI Summary",
                        id=f"ai-summary-btn-{page_key}",
                        variant="filled",
                        size="sm",
                    ),
                ],
            ),
            dmc.Text(
                "Click to generate a concise page summary.",
                id=f"ai-summary-output-{page_key}",
                mt="sm",
                size="sm",
            ),
        ]
    )
