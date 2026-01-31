from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# ---------- Load Vector Store ----------
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ---------- Load Persona ----------
with open("knowledge/bio/persona.md") as f:
    persona = f.read()

with open("knowledge/bio/tone.md") as f:
    tone = f.read()

with open("knowledge/bio/boundaries.md") as f:
    boundaries = f.read()

SYSTEM_PROMPT = f"""
{persona}

{tone}

{boundaries}

Rules:
- Use context for facts
- Be honest if context is missing
- No generic advice
"""

# ---------- Prompt ----------
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """
Context:
{context}

Question:
{question}
""")
])

# ---------- Model ----------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

# ---------- Chain ----------
rag_chain = (
    {
        "context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)),
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# ---------- Test ----------
questions = [
    "Why did you choose RAG instead of fine-tuning?",
    "How strong are you in NLP?",
    "How do you handle failure?",
    "Explain Kubernetes",
    "What are you bad at?"
]

for q in questions:
    print("\nQ:", q)
    print("A:", rag_chain.invoke(q))