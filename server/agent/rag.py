import os

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langfuse import Langfuse
from agent.vectorstore.retriever import pinecone_retriever

from dotenv import load_dotenv
load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")
langfuse = Langfuse()

langfuse_prompt = langfuse.get_prompt("oriencoop-rag-qa")
question_generation_prompt = langfuse.get_prompt("oriencoop-question-suggestions")
langchain_prompt = ChatPromptTemplate.from_template(
    langfuse_prompt.get_langchain_prompt())


def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        filename = doc.metadata.get('filename', 'Documento desconocido')
        page_number = doc.metadata.get('page_number', 'N/A')
        content = f"[Archivo: {filename}, Página: {page_number}]\n{doc.page_content}"
        formatted_docs.append(content)
    return "\n\n".join(formatted_docs)


llm = ChatOpenAI(model="gpt-4o")


def get_retriever():
    retriever = RunnableLambda(pinecone_retriever)
    return retriever


def retrieve_documents(input_dict):
    question = input_dict["question"]
    retriever = get_retriever()
    docs = retriever.invoke(question)
    formatted_docs = format_docs(docs)
    return formatted_docs


def get_question(input_dict):
    return input_dict["question"]


def format_chat_history(chat_history, max_messages=5):
    formatted_history = []
    for message in chat_history[-max_messages:]:
        if isinstance(message, HumanMessage):
            role = "Usuario"
        elif isinstance(message, AIMessage):
            role = "Asistente"
        else:
            role = "Sistema"
        formatted_message = f"{role}: {message.content}"
        formatted_history.append(formatted_message)
    return "\n".join(formatted_history)


def get_chat_history(input_dict):
    chat_history = input_dict["chat_history"]
    return format_chat_history(chat_history)


rag_chain = RunnableParallel({
    "context": retrieve_documents,
    "question": get_question,
    "chat_history": get_chat_history,
}) | langchain_prompt | llm