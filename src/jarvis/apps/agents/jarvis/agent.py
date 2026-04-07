from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from jarvis.apps.agents.jarvis.llm import llm
from jarvis.apps.agents.jarvis.state import AgentState
from jarvis.core.mcp_manager import mcp_manager


class Agent:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("chatbot", self._call_model)
        workflow.add_node("tools", self._execute_tools)

        workflow.add_edge(START, "chatbot")
        workflow.add_conditional_edges("chatbot", self._should_continue)
        workflow.add_edge("tools", "chatbot")

        return workflow.compile()

    def _execute_tools(self, state: AgentState):
        node = ToolNode(mcp_manager.tools)
        return node.invoke(state)

    def _call_model(self, state: AgentState):
        system_message = SystemMessage(
            content="You are Jarvis, a helpful assistant. You have access to tools for calendar events and Todoist tasks. "
                    "Your goal is to gather these and format them nicely in plain text so they can be sent to the user via Telegram."
        )
        messages = [system_message] + list(state["messages"])
        
        if mcp_manager.tools:
            llm_with_tools = self.llm.bind_tools(mcp_manager.tools)
        else:
            llm_with_tools = self.llm
            
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def _should_continue(self, state: AgentState):
        last_message = state["messages"][-1]
        return "tools" if last_message.tool_calls else END


agent = Agent(
    llm=llm,
)
