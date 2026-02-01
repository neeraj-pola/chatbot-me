from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal
from fastapi.responses import StreamingResponse
import json
from rag.chain import build_rag_chain

app = FastAPI()

# --------------------
# CORS (important for Vercel)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Request models
# --------------------
class ChatMessage(BaseModel):
    role: Literal["user", "bot"]
    content: str


class ChatRequest(BaseModel):
    question: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    answer: str


# --------------------
# Helpers
# --------------------
def format_history(history: List[ChatMessage]) -> str:
    """
    Convert message list into a readable conversation transcript
    """
    lines = []
    for msg in history:
        if msg.role == "user":
            lines.append(f"User: {msg.content}")
        else:
            lines.append(f"Assistant: {msg.content}")
    return "\n".join(lines)


# --------------------
# Build RAG chain once
# --------------------
rag_chain = build_rag_chain()


# --------------------
# Routes
# --------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    question = req.question
    history_text = format_history(req.history)

    result = rag_chain.invoke(
        {
            "question": question,
            "chat_history": history_text,
        }
    )

    return {"answer": result}


@app.post("/chat-stream")
async def chat_stream(req: ChatRequest):
    question = req.question
    history_text = format_history(req.history)

    def event_generator():
        try:
            for chunk in rag_chain.stream(
                {
                    "question": question,
                    "chat_history": history_text,
                }
            ):
                # Send token chunk to client
                yield f"data: {json.dumps({'token': chunk})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

        # Signal completion
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )