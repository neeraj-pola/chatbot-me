from dotenv import load_dotenv
load_dotenv()

from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from rag.persona import load_persona
from rag.retriever import load_retriever


def build_rag_chain():
    persona = load_persona()
    retriever = load_retriever(k=4)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        streaming=True,  # enabled, but not used yet
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", persona),
        ("system", "Conversation so far:\n{chat_history}"),
        ("human", """
Context:
{context}

Question:
{question}
"""),
    ])

    def format_docs(docs):
        if not docs:
            return "No relevant context found."
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            # 🔑 ONLY pass question to retriever
            "context": itemgetter("question") | retriever | format_docs,

            # These pass through untouched
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain