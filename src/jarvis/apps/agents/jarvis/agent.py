from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from jarvis.apps.agents.jarvis.llm import llm
from jarvis.apps.agents.jarvis.state import AgentState


class Agent:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.tools = []
        self.graph = self._build_graph()

    async def fetch_mcp_tools(self, server_params: StdioServerParameters):
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                mcp_tools = await session.list_tools()
                return mcp_tools

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("chatbot", self._call_model)
        workflow.add_node("tools", ToolNode(self.tools))

        workflow.add_edge(START, "chatbot")
        workflow.add_conditional_edges("chatbot", self._should_continue)
        workflow.add_edge("tools", "chatbot")

        return workflow.compile()

    def _call_model(self, state: AgentState):
        response = self.llm.bind_tools(self.tools).invoke(state["messages"])
        return {"messages": [response]}

    def _should_continue(self, state: AgentState):
        last_message = state["messages"][-1]
        return "tools" if last_message.tool_calls else END


agent = Agent(
    llm=llm,
)
