import mcp.types as types

from jarvis.apps.todoist.app import mcp


@mcp.tool(
    name="get_today_tasks",
    description=(
        ""
    ),
)
def get_today_tasks(self):
    tasks_mock = ["Buy a bread", "Prepare for the interview"]

    return [
        types.TextContent(
            type="text",
            text=f"Todoist tasks:\n" + "\n".join(tasks_mock)
        )
    ]
