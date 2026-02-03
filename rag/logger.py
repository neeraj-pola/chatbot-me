import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # service role key

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def log_chat(
    session_id,
    role: str,
    message: str,
    is_small_talk: bool,
    used_retrieval: bool,
    latency_ms: int | None,
):
    """
    Logs a single chat message (user OR assistant).
    One row per utterance.
    """
    supabase.table("chat_logs").insert({
        "session_id": str(session_id),
        "role": role,
        "message": message,
        "is_small_talk": is_small_talk,
        "used_retrieval": used_retrieval,
        "latency_ms": latency_ms,
    }).execute()