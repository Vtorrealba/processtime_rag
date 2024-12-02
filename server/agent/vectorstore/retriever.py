import os 
from datetime import datetime
import uuid
from pinecone import Pinecone 
from pinecone import ServerlessSpec
from langfuse import Langfuse 
from openai import OpenAI

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGUSE_PRIVATE_KEY")
)
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
spec = ServerlessSpec(cloud='aws', region='us-east-1')

index = pc.Index('oriencoop-rag-qa')

def pinecone_retriever(text:str) -> list[Document]:
    trace_id = str(uuid.uuid4())
    trace = langfuse.trace(
        id = trace_id,
        name="pinecone-retriever",
        session_id=str(uuid.uuid4()),
        timestamp=datetime.now(),
        input=text,
        model="text-embedding-3-large"
        )
    
    text = text.replace("\n", " ")
    embed_event = trace.span(start_time=datetime.now(), name="embed-query", input=text)
    res = openai.embeddings.create(
        model="text-embedding-3-large",
        input= [text]

    )
    emb = res.data[0].embedding
    trace.update(usage = res.usage)
    embed_event.update(end_time=datetime.now(),output=emb, model="text-embedding-3-large")

    top_k=4

    retrieve_span = trace.span(name = "retrieve_documents", input=text, start_time=datetime.now())    
    res = index.query(vector=emb, top_k=top_k, include_metadata=True)
    docs = []
    matches = res["matches"]
    similarity_scores = []
    for match in matches:
        similarity_scores.append(match["score"])
        doc = Document(
            id = match["id"],
            page_content=match["metadata"]["text"],
            metadata = {
                "page_number" : str(match["metadata"]["page_number"]),
                "filename": match["metadata"]["filename"],
                "score": match["score"]
            }
        )
        document_event = retrieve_span.event(
            id=str(uuid.uuid4()),
            name="document", 
            input=text, 
            output=doc.page_content, 
            metadata=doc ,
            start_time=datetime.now()
            )
        docs.append(doc)

        document_event.score(
            name="similarity",
            value=doc.metadata["score"],
            data_type="NUMERIC"
        )

    trace.score(
        trace_id = trace_id,
        name="avg-similarity",
        value=sum(similarity_scores) / len(matches),
        data_type="NUMERIC"
    )
    retrieve_span.update(output=docs, end_time=datetime.now(), score = (sum(similarity_scores) / len(matches)))

    trace.update(output=docs)

    return docs








