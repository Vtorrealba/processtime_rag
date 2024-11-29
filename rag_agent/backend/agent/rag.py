import os

from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY")
langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

langfuse_handler = CallbackHandler(
    secret_key=langfuse_secret,
    public_key=langfuse_public,
    host="https://us.cloud.langfuse.com",
)

langfuse = Langfuse()

langfuse_prompt = langfuse.get_prompt("legal-expert")
question_generation_prompt = langfuse.get_prompt("question_generation")
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

config = {
    "callbacks": [langfuse_handler],
    "run_name": "legal_expert_Q&A_citations",
    "session_id": "legal_expert_Q&A"
}


def get_retriever():
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory='db', embedding_function=embeddings)
    retriever = vectordb.as_retriever()
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
}) | langchain_prompt | llm | StrOutputParser()