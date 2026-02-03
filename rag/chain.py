from dotenv import load_dotenv
load_dotenv()

from operator import itemgetter
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from rag.persona import load_persona
from rag.retriever import load_retriever


# --------------------
# Load long-term bio
# --------------------
def load_bio_context() -> str:
    """
    Loads all personal/background markdown files.
    Injected as long-term memory.
    """
    bio_dir = Path("knowledge/bio")
    parts = []

    if bio_dir.exists():
        for file in sorted(bio_dir.glob("*.md")):
            parts.append(file.read_text())

    return "\n\n".join(parts) if parts else ""


# --------------------
# Build RAG chain
# --------------------
def build_rag_chain():
    persona = load_persona()
    retriever = load_retriever(k=6)
    bio_context = load_bio_context()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.6,
        streaming=True,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", persona),
        ("system", "Conversation so far:\n{chat_history}"),
        (
            "human",
            """Context:
{context}

Question:
{question}"""
        ),
    ])

    # -------- Format retrieved docs (ONE pass) --------
    def format_docs(docs):
        retrieved_text = "\n\n".join(doc.page_content for doc in docs) if docs else ""
        return {
            "context": f"""
=== PERSONAL BACKGROUND (use ONLY if relevant) ===
{bio_context}

=== RETRIEVED CONTEXT ===
{retrieved_text}
""",
            "retrieved_chunks_count": len(docs) if docs else 0,
        }

    format_docs_runnable = RunnableLambda(format_docs)

    rag_chain = (
        {
            "retrieval": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | RunnableLambda(
            lambda x: {
                **x,
                **format_docs(x["retrieval"]),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain