from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.chain import build_rag_chain


app = FastAPI(title="Neeraj RAG Bot")

# -------------------------
# CORS — MUST be before routes
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   # IMPORTANT: allows OPTIONS
    allow_headers=["*"],
)

# -------------------------
# Load RAG chain ONCE
# -------------------------
rag_chain = build_rag_chain()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = rag_chain.invoke(req.question)
    return {"answer": answer}