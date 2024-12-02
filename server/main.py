from fastapi import FastAPI, Request, Form, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent.workflow import agent_graph, config
from fastapi.middleware.cors import CORSMiddleware




class SimpleRequest(BaseModel):
    """
    Esquema para endpoint de prueba interna
    
    request ejemplo
    json
    {
        question: "prueba"
    }
    """
    question: str


app = FastAPI(
    title="Oriencoop RAG Agent",
    description="An agent built on top of LangGraph and LangChain that uses RAG to leverage corporate knowledge and answer questions",
    version="0.1.0",
)

origins = [
    "http://localhost:4173",
    "http://localhost:5173/",
    "http://18.230.75.174:4173",
    "http://18.230.75.174",
    "http://18.230.75.174:80",
    "https://oriencoop-rag.click"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/ask-dev")
async def reply(request: SimpleRequest) -> dict[str, str]:
    """
    Endpoint para prueba interna
    envia una SimpleRequest
    
    retorna -> {"content": "string" }
    """
    response = agent_graph.invoke({"messages": [HumanMessage(content=request.question)]}, config = config)
    agent_response =  response["messages"][-1].content
    return {"content": agent_response}
    
    

