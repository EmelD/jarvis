import mcp.types as types

from jarvis.apps.google_calendar.app import mcp


@mcp.tool(
    name="get_today_events",
    description=(
        ""
    ),
)
async def get_today_events() -> list[types.TextContent]:
    events_mock = ["10:00 - Daily Sync", "14:00 - Interview with HR"]

    return [
        types.TextContent(
            type="text",
            text=f"Today events:\n" + "\n".join(events_mock)
        )
    ]
