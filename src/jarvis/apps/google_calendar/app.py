from mcp.server import FastMCP
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response


app = FastMCP("Google Calendar MCP")


@app.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> Response:
    return JSONResponse({"status": "ok"})
