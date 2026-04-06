import logging
import httpx
from enum import Enum
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from langchain_core.tools import Tool

logger = logging.getLogger(__name__)


class ServerStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    INITIALIZING = "initializing"


class MCPManager:
    def __init__(self):
        self._server_registry = {}
        self.server_statuses = {}
        self.tools = []
        self._exit_stack = AsyncExitStack()

    async def check_health(self):
        async with httpx.AsyncClient() as client:
            for name, url in self._server_registry.items():
                try:
                    response = await client.get(url.replace("/sse", "/health"), timeout=2.0)
                    if response.status_code == 200:
                        if self.server_statuses[name] == ServerStatus.OFFLINE:
                            logger.info(f"Server {name} is available. Reconnecting...")
                            await self._reconnect_server(name)
                        self.server_statuses[name] = ServerStatus.ONLINE
                    else:
                        self.server_statuses[name] = ServerStatus.OFFLINE
                except Exception:
                    if self.server_statuses[name] == ServerStatus.ONLINE:
                        logger.warning(f"Server {name} is lost.")
                    self.server_statuses[name] = ServerStatus.OFFLINE

    async def _reconnect_server(self, name: str):
        pass

    def register_server(self, name: str, url: str):
        self._server_registry[name] = url
        self.server_statuses[name] = ServerStatus.OFFLINE
        logger.info(f"Server '{name}' has been added to MCP registry.")

    async def start_all(self):
        if not self._server_registry:
            logger.warning("There are no MCP servers.")
            return

        logger.info(f"Starting {len(self._server_registry)} MCP servers...")

        started = 0
        for name, url in self._server_registry.items():
            try:
                # connection logic

                started += 1
                logger.info(f"MCP server '{name}' has been started.")
            except Exception as e:
                logger.error(f"Error on starting '{name}' MCP server: {e}")

        logger.info(f"{started} MCP servers has been started.")

    def _make_langchain_tool(self, session: ClientSession, mcp_tool):
        async def call_tool(arguments: dict):
            result = await session.call_tool(mcp_tool.name, arguments=arguments)
            return result.content

        return Tool(
            name=mcp_tool.name,
            func=call_tool,
            description=mcp_tool.description
        )

    async def stop_all(self):
        logger.info("Stopping all MCP servers...")
        await self._exit_stack.aclose()
        self.tools.clear()
        logger.info("All MCP servers has been closed.")


mcp_manager = MCPManager()
