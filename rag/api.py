from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Literal
import json
import time
import uuid

from rag.chain import build_rag_chain
from rag.logger import log_chat


# --------------------
# Small talk detection
# --------------------
SMALL_TALK = {
    "hi", "hello", "hey", "hey there",
    "how are you", "how r u", "sup", "what's up"
}


# --------------------
# App
# --------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------
# Models
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
    if not history:
        return ""

    return "\n".join(
        f"{'User' if m.role == 'user' else 'Assistant'}: {m.content}"
        for m in history
    )


def is_small_talk(text: str) -> bool:
    return text.strip().lower() in SMALL_TALK


# --------------------
# Build chain ONCE
# --------------------
rag_chain = build_rag_chain()


# --------------------
# Routes
# --------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    start_time = time.time()
    session_id = uuid.uuid4()

    question = req.question.strip()
    small_talk = is_small_talk(question)

    payload = {
        "question": question,
        "chat_history": "" if small_talk else format_history(req.history),
    }

    answer = rag_chain.invoke(payload)
    latency_ms = int((time.time() - start_time) * 1000)

    # ---- LOG USER MESSAGE ----
    log_chat(
        session_id=session_id,
        role="user",
        message=question,
        is_small_talk=small_talk,
        used_retrieval=not small_talk,
        latency_ms=None,
    )

    # ---- LOG ASSISTANT MESSAGE ----
    log_chat(
        session_id=session_id,
        role="assistant",
        message=answer,
        is_small_talk=small_talk,
        used_retrieval=not small_talk,
        latency_ms=latency_ms,
    )

    return {"answer": answer}


@app.post("/chat-stream")
async def chat_stream(req: ChatRequest):
    start_time = time.time()
    session_id = uuid.uuid4()

    question = req.question.strip()
    small_talk = is_small_talk(question)

    payload = {
        "question": question,
        "chat_history": "" if small_talk else format_history(req.history),
    }

    collected_chunks: list[str] = []

    # log user immediately
    log_chat(
        session_id=session_id,
        role="user",
        message=question,
        is_small_talk=small_talk,
        used_retrieval=not small_talk,
        latency_ms=None,
    )

    def event_generator():
        try:
            for chunk in rag_chain.stream(payload):
                collected_chunks.append(chunk)
                yield f"data: {json.dumps({'token': chunk})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

        latency_ms = int((time.time() - start_time) * 1000)

        # log assistant once streaming finishes
        log_chat(
            session_id=session_id,
            role="assistant",
            message="".join(collected_chunks),
            is_small_talk=small_talk,
            used_retrieval=not small_talk,
            latency_ms=latency_ms,
        )

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )