from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def load_retriever(k: int = 4):
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(
        search_type="mmr",  # better diversity
        search_kwargs={
            "k": k,
            "fetch_k": max(10, k * 3),  # wider candidate pool
            "lambda_mult": 0.7,         # balance relevance vs diversity
        }
    )