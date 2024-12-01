import os
from datetime import datetime
from typing import Annotated, Sequence, List, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph.state import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from agent.rag import rag_chain
from langfuse.callback import CallbackHandler


langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY")
langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_handler = CallbackHandler(
    secret_key=langfuse_secret,
    public_key=langfuse_public,
    host="https://us.cloud.langfuse.com",
)

from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages

from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]
    last_user_message: Optional[HumanMessage]

# def agent(state: AgentState) -> AgentState:
    
#     if len(state["messages"]) == 1:
#         question = state["messages"][0].content
#         assert state["messages"][0].type == "human"
#     else:
#         question = state["messages"][-1].content
#         assert state["messages"][-1].type == "human"
#         assert state["messages"][-2].type == "ai"

#     if len(state["messages"]) > 10:
#         chat_history = state["messages"][-10:]
#     else:
#         chat_history = state["messages"]

#     return {
#             "messages": [
#             rag_chain.invoke({"question": question, "chat_history": chat_history}, config=config)
#         ]
#     }


def compute_last_user_message(state: AgentState) -> Optional[HumanMessage]:
    """
    Computes the last user message from the state.
    """
    for message in reversed(state["messages"]):
        if message.type == "human":
            return message
    return None  # Return None if no user message is found

def update_state_with_last_user_message(state: AgentState) -> AgentState:
    """
    Updates the state with the last user message.
    """
    last_user_message = compute_last_user_message(state)
    state["last_user_message"] = last_user_message
    return state

def agent(state: AgentState) -> AgentState:
    state = update_state_with_last_user_message(state)

    if not state["last_user_message"]:
        raise ValueError("No user message found in the state.")

    question = state["last_user_message"].content
    if state["last_user_message"].type != "human":
        raise ValueError("The 'last_user_message' should be a human message")
    chat_history = state["messages"][-10:] if len(state["messages"]) > 10 else state["messages"]

    result = rag_chain.invoke({"question": question, "chat_history": chat_history}, config=config)

    return {
        "messages": state["messages"] + [result],
        "last_user_message": state["last_user_message"],
    }

workflow = StateGraph(AgentState)


workflow.add_node("agent", agent)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

memory = MemorySaver()

agent_graph = workflow.compile(checkpointer=memory)

config = {
    "configurable": {"thread_id": "1"},
    "callbacks": [langfuse_handler],
    "run_name": "oriencoop_RAG_QA",
    "session_id": "oriencoop_RAG_QA"
}

# OriencoopRag = {
#     "agent_config": config,
#     "agent": agent_graph
# }

# # Interactive chat loop
# print("Welcome to the Oriencoop chatbot! Type 'exit' to end the conversation.")

# while True:
#     # Get user input
#     user_input = input("\nYou: ")
    
#     # Check for exit condition
#     if user_input.lower() == 'exit':
#         print("Goodbye!")
#         break
        
#     # Create human message and invoke graph
#     human_message = HumanMessage(content=user_input)
    
#     try:
#         # Record start time
#         start_time = datetime.now()
        
#         # Get response
#         response = graph.invoke({"messages": [human_message]}, config=config)
        
#         # Calculate duration
#         duration = (datetime.now() - start_time).total_seconds()
        
#         # Print response
#         print(f"\nBot (responded in {duration:.2f}s): {response['messages'][-1].content}")
        
#     except Exception as e:
#         print(f"\nError: {str(e)}")


