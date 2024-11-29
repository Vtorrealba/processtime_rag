from typing import Annotated, Sequence
from typing_extensions import TypedDict
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph.state import END, StateGraph, START
from langgraph.prebuilt import ToolNode


from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


workflow = StateGraph(AgentState)

workflow.add_node("agent", agent)
workflow.add_node("generate", generate)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile()

