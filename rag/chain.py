from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from rag.persona import load_persona
from rag.retriever import load_retriever

def build_rag_chain():
    persona = load_persona()
    retriever = load_retriever(k=4)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", persona),
        ("human", """
Context:
{context}

Question:
{question}
""")
    ])

    def format_docs(docs):
        if not docs:
            return "No relevant context found."
        return "\n\n".join(d.page_content for d in docs)

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain