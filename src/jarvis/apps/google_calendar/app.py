from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from mcp.server import FastMCP


mcp = FastMCP(
    name="Google Calendar MCP",
    stateless_http=True,
    json_response=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/v1", mcp.streamable_http_app())


@app.get("/health")
async def health_check() -> Response:
    return JSONResponse({"status": "ok"})
