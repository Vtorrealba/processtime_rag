from fastapi import FastAPI, Request, Form, Depends

app = FastAPI(
    title="Oriencoop RAG Agent",
    description="An agent built on top of LangGraph and LangChain that uses RAG to leverage corporate knowledge and answer questions",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/message")
async def reply(request: Request, Body: str = Form(), db: Session = Depends(get_db)):
    form_data = await request.form()

