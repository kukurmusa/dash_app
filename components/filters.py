import dash_mantine_components as dmc


def labelled_select(label: str, component_id: str, data, value=None, searchable=False):
    return dmc.Stack(
        gap=4,
        children=[
            dmc.Text(label, size="sm", fw=500),
            dmc.Select(
                id=component_id,
                data=data,
                value=value,
                searchable=searchable,
            ),
        ],
    )
