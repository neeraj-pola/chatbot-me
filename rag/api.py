from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

from rag.chain import build_rag_chain

app = FastAPI(title="Neeraj RAG Bot")

rag_chain = build_rag_chain()  # loaded ONCE at startup


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = rag_chain.invoke(req.question)
    return {"answer": answer}